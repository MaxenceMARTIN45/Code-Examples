# notifications.py

import asyncio


class NotificationManager:
    def __init__(self):
        self.clients = {}

    def _get_clients_set(self, event_type):
        if event_type not in self.clients:
            self.clients[event_type] = set()
        return self.clients[event_type]

    async def handle_websocket(self, websocket, event_type):
        clients_set = self._get_clients_set(event_type)
        clients_set.add(websocket._get_current_object())
        try:
            while True:
                await websocket.receive()  # Keep the connection alive
        finally:
            clients_set.remove(websocket._get_current_object())

    async def notify_clients(self, message, event_type):
        clients_set = self._get_clients_set(event_type)
        if clients_set:
            await asyncio.gather(
                *(client.send(message) for client in clients_set)
            )
