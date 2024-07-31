# file_watcher.py

import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileModificationHandler(FileSystemEventHandler):
    def __init__(self, loop, notification_handler):
        self.loop = loop
        self.notification_handler = notification_handler

    def on_created(self, event):
        print(f"File created: {event.src_path}")
        asyncio.run_coroutine_threadsafe(
            self.notification_handler.notify("create", event.src_path),
            self.loop,
        )

    def on_modified(self, event):
        print(f"File modified: {event.src_path}")
        asyncio.run_coroutine_threadsafe(
            self.notification_handler.notify("modify", event.src_path),
            self.loop,
        )

    def on_deleted(self, event):
        print(f"File deleted: {event.src_path}")
        asyncio.run_coroutine_threadsafe(
            self.notification_handler.notify("delete", event.src_path),
            self.loop,
        )


def start_watchdog(path, loop, notification_handler):
    event_handler = FileModificationHandler(loop, notification_handler)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    observer.join()  # Blocks in a separate thread
