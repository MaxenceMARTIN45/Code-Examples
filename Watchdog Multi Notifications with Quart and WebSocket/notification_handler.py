# notification_handler.py


class NotificationHandler:
    def __init__(self):
        self.handlers = {}

    def add_handler(self, event_type, notify_callback):
        self.handlers[event_type] = notify_callback

    def get_handler(self, event_type):
        return self.handlers.get(event_type, None)

    async def notify(self, event_type, message):
        handler = self.get_handler(event_type)
        if handler:
            await handler(message)
        else:
            print(f"No handler for event type: {event_type}")
