# application.py

import asyncio
import threading
from quart import Quart, websocket, render_template
from notification_manager import NotificationManager
from file_watcher import start_watchdog
from notification_handler import NotificationHandler
from config import PATH_TO_WATCH, BIND_ADDRESS

application = Quart(__name__)
notification_manager = NotificationManager()

# Setup notification handler
notification_handler = NotificationHandler()


async def handle_create(msg):
    await notification_manager.notify_clients(msg, "create")


async def handle_modify(msg):
    await notification_manager.notify_clients(msg, "modify")


async def handle_delete(msg):
    await notification_manager.notify_clients(msg, "delete")


notification_handler.add_handler("create", handle_create)
notification_handler.add_handler("modify", handle_modify)
notification_handler.add_handler("delete", handle_delete)


@application.route("/")
async def index():
    return await render_template("index.html")


@application.websocket("/ws/<event_type>")
async def ws(event_type):
    await notification_manager.handle_websocket(websocket, event_type)


@application.before_serving
async def start_watchdog_thread():
    loop = asyncio.get_event_loop()
    watchdog_thread = threading.Thread(
        target=start_watchdog,
        args=(PATH_TO_WATCH, loop, notification_handler),
    )
    watchdog_thread.daemon = True
    watchdog_thread.start()


if __name__ == "__main__":
    import hypercorn.asyncio
    import hypercorn.config

    config = hypercorn.config.Config()
    config.bind = [BIND_ADDRESS]

    asyncio.run(hypercorn.asyncio.serve(application, config))
