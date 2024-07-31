import asyncio
import threading
from quart import Quart, websocket, render_template
from websocket_manager import WebSocketManager
from file_watcher import start_watchdog
from config import PATH_TO_WATCH, BIND_ADDRESS

application = Quart(__name__)
ws_manager = WebSocketManager()


@application.route("/")
async def index():
    return await render_template("index.html")


@application.websocket("/ws")
async def ws():
    await ws_manager.handle_websocket(websocket)


@application.before_serving
async def start_watchdog_thread():
    loop = asyncio.get_event_loop()
    watchdog_thread = threading.Thread(
        target=start_watchdog,
        args=(PATH_TO_WATCH, loop, ws_manager.notify_clients),
    )
    watchdog_thread.daemon = True
    watchdog_thread.start()


if __name__ == "__main__":
    import hypercorn.asyncio
    import hypercorn.config

    config = hypercorn.config.Config()
    config.bind = [BIND_ADDRESS]

    asyncio.run(hypercorn.asyncio.serve(application, config))
