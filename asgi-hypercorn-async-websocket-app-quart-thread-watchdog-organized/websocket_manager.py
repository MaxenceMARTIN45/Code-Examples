import asyncio


class WebSocketManager:
    def __init__(self):
        self.clients = set()

    async def handle_websocket(self, websocket):
        self.clients.add(websocket._get_current_object())
        try:
            while True:
                await websocket.receive()  # Keep the connection alive
        finally:
            self.clients.remove(websocket._get_current_object())

    async def notify_clients(self, message):
        if self.clients:
            await asyncio.gather(
                *(client.send(message) for client in self.clients)
            )
