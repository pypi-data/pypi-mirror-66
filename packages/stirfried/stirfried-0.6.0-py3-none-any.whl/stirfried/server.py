from celery import Celery, Signature
from celery.result import AsyncResult
from celery.states import FAILURE
import socketio
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route


# LOAD CONFIG


celery_app = Celery()
CONFIG_MODULE = "settings"
celery_app.config_from_object(CONFIG_MODULE)
redis_url = celery_app.conf.get("stirfried_redis_url", "")
available_tasks = set(celery_app.conf.get("stirfried_available_tasks", []))
error_info = celery_app.conf.get("stirfried_error_info", False)
sentinel_room = celery_app.conf.get("stirfried_sentinel_room", "NO_EMIT")
custom_rooms = celery_app.conf.get("stirfried_custom_rooms", False)
header_task_map = celery_app.conf.get("stirfried_header_task_map", {})
enable_http = celery_app.conf.get("stirfried_enable_http", True)
enable_socketio = celery_app.conf.get("stirfried_enable_socketio", True)
enable_task_info = celery_app.conf.get("stirfried_enable_task_info", True)
enable_revoke_task = celery_app.conf.get("stirfried_enable_revoke_task", True)

socketio_opts = {
    key[9:]: value
    for key, value in celery_app.conf.items()
    if key.startswith("socketio_")
}


# COMMON LOGIC


def filter_headers(headers):
    mapped_headers = {
        header
        for header_map in header_task_map.values()
        for header in header_map.keys()
    }
    return {k: v for k, v in headers.items() if k in mapped_headers}


def parse_task(sid, message, headers):
    # task_name
    task_name = message["task_name"]
    if len(available_tasks) > 0 and task_name not in available_tasks:
        raise KeyError(task_name)
    # args
    args = message.get("args", ())
    # kwargs
    sid_kwarg = message.get("room", sid) if custom_rooms else sid
    header_map = header_task_map.get(task_name, {})
    header_kwargs = {header_map[k]: v for k, v in headers.items() if k in header_map}
    kwargs = {
        **message.get("kwargs", {}),
        **header_kwargs,
        "room": sid_kwarg,
    }
    # chain
    chain = [
        Signature(c_task_name, args=c_args, kwargs=c_kwargs)
        for c_task_name, c_args, c_kwargs, _ in [
            parse_task(sid, c, headers) for c in message.get("chain", [])
        ]
    ]
    return task_name, args, kwargs, chain


def create_task(sid, message, headers):
    try:
        task_name, args, kwargs, chain = parse_task(sid, message, headers)
    except KeyError as err:
        return dict(status="failed", data=f"unknown task {str(err)}")
    t = celery_app.send_task(task_name, args=args, kwargs=kwargs, chain=chain)
    return dict(status="success", data=t.id)


def delete_task(task_id):
    celery_app.control.revoke(task_id)


def get_task_info(task_id):
    return AsyncResult(task_id, app=celery_app)


# HTTP API


async def http_send_task(request):
    headers = {k.lower().replace("_", "-"): v for k, v in request.headers.items()}
    headers = filter_headers(headers)
    message = await request.json()
    result = create_task(sentinel_room, message, headers)
    status = 400 if result["status"] == "failure" else 201
    return JSONResponse(result, status_code=status)


async def http_task_info(request):
    task_id = request.path_params["task_id"]
    async_result = get_task_info(task_id)
    status = 200
    result = async_result.result
    if async_result.state == FAILURE:
        result = str(result) if error_info else None
        status = 500
    return JSONResponse(
        {"id": async_result.id, "state": async_result.state, "result": result},
        status_code=status,
    )


async def http_revoke_task(request):
    task_id = request.path_params["task_id"]
    delete_task(task_id)
    return Response()


def create_http_app():
    routes = []
    routes.append(Route("/task", http_send_task, methods=["POST"]))
    if enable_task_info:
        routes.append(Route("/task/{task_id}", http_task_info, methods=["GET"]))
    if enable_revoke_task:
        routes.append(Route("/task/{task_id}", http_revoke_task, methods=["DELETE"]))
    return Starlette(debug=error_info, routes=routes,)


# SOCKET.IO API


sio = None


def socketio_revoke_task(sid, message):
    """Call to revoke a task from the worker fleet."""
    delete_task(message)


async def socketio_send_task(sid, message: dict):
    """Call to send a task to the worker fleet."""
    headers = await sio.get_session(sid)
    return create_task(sid, message, headers)


async def socketio_task_info(sid, message: dict):
    """Call to request info on a task."""
    async_result = get_task_info(message)
    result = async_result.result
    if async_result.state == FAILURE:
        result = str(result) if error_info else None
    return {"id": async_result.id, "state": async_result.state, "result": result}


async def socketio_connect(sid, environ):
    prefix = f"HTTP_"
    headers = {
        k[len(prefix) :].lower().replace("_", "-"): v
        for k, v in environ.items()
        if k.startswith(prefix)
    }
    headers = filter_headers(headers)
    await sio.save_session(sid, headers)


def create_socketio_app(**kwargs):
    global sio
    mgr = socketio.AsyncRedisManager(redis_url)
    sio = socketio.AsyncServer(client_manager=mgr, async_mode="asgi", **socketio_opts)
    sio.on("connect", socketio_connect)
    sio.on("send_task", socketio_send_task)
    if enable_revoke_task:
        sio.on("revoke_task", socketio_revoke_task)
    if enable_task_info:
        sio.on("task_info", socketio_task_info)
    return socketio.ASGIApp(sio, **kwargs)


# ASGI APP


if enable_http and enable_socketio:
    app = create_socketio_app(other_asgi_app=create_http_app())
elif enable_socketio:
    app = create_socketio_app()
elif enable_http:
    app = create_http_app()
