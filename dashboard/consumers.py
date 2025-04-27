import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CryptoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "crypto-prices"

        # Join WebSocket group (only once)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept WebSocket connection (only once)
        await self.accept()

        print("WebSocket connected to group: crypto-prices")


    async def disconnect(self, close_code):
        # Leave WebSocket group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):  # Change to async
        print("Received data from client:", text_data)  # Debugging log
        await self.send(text_data=json.dumps({
            'message': "Hello from server!"
        }))

    async def send_crypto_data(self, event):
        # This is where we get Fluvio data and send it to the WebSocket
        message = event['message']
        print("Sending data to WebSocket:", message)

        # Send data to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))