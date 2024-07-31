import asyncio
import threading
from quart import Quart, websocket, render_template
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

application = Quart(__name__)
clients = set()
loop = None  # Event loop global


@application.route("/")
async def index():
    return await render_template("index.html")


class MyHandler(FileSystemEventHandler):
    def __init__(self, loop):
        self.loop = loop

    def on_modified(self, event):
        print(f"Modification detected: {event.src_path}")
        # Envoyer une notification à tous les clients WebSocket connectés
        asyncio.run_coroutine_threadsafe(
            notify_clients(event.src_path), self.loop
        )


async def notify_clients(message):
    if clients:
        await asyncio.gather(*(client.send(message) for client in clients))


@application.websocket("/ws")
async def ws():
    clients.add(websocket._get_current_object())
    try:
        while True:
            await websocket.receive()  # Keep the connection alive
    finally:
        clients.remove(websocket._get_current_object())


def start_watchdog(path, loop):
    event_handler = MyHandler(loop)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    observer.join()  # Bloque dans un thread séparé


@application.before_serving
async def start_watchdog_thread():
    global loop
    path_to_watch = "history"  # Changez cela pour le chemin à surveiller

    # Obtenir l'event loop principal et le passer au thread Watchdog
    loop = asyncio.get_event_loop()

    watchdog_thread = threading.Thread(
        target=start_watchdog, args=(path_to_watch, loop)
    )
    watchdog_thread.daemon = True
    watchdog_thread.start()


# Lancer l'applicationlication Quart avec Hypercorn
if __name__ == "__main__":
    import hypercorn.asyncio
    import hypercorn.config

    config = hypercorn.config.Config()
    config.bind = ["0.0.0.0:8000"]

    asyncio.run(hypercorn.asyncio.serve(application, config))
