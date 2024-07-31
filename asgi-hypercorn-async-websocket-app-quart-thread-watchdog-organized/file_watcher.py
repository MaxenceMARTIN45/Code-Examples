import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileModificationHandler(FileSystemEventHandler):
    def __init__(self, loop, notify_callback):
        self.loop = loop
        self.notify_callback = notify_callback

    def on_modified(self, event):
        print(f"Modification detected: {event.src_path}")
        asyncio.run_coroutine_threadsafe(
            self.notify_callback(event.src_path), self.loop
        )


def start_watchdog(path, loop, notify_callback):
    event_handler = FileModificationHandler(loop, notify_callback)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    observer.join()  # Blocks in a separate thread
