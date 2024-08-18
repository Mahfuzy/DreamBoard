from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class GroupChatConsumer(WebsocketConsumer):
    def connect(self):
        # Get the room name from the URL path
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print(f"WebSocket connected to room {self.room_name}")
        print(f"Websocket connected to {self.channel_name}")

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected from room {self.room_name}")
        print(f"Websocket disconnected from {self.channel_name}")

    def receive(self, text_data):
        print(f"Received data: {text_data}")
        print(f"{self.channel_name} received message {text_data}")

        # Broadcast message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data
            }
        )

    def chat_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        self.send(text_data=message)

class DirectChatConsumer(WebsocketConsumer):
    def connect(self):
        # Get the sender and recipient usernames
        self.sender = self.scope['user'].username
        self.recipient = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'direct_{self.sender}_{self.recipient}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print(f"WebSocket connected to room {self.room_group_name}")
        print(f"WebSocket connected to {self.channel_name}")

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected from room {self.room_group_name}")
        print(f"WebSocket disconnected from {self.channel_name}")

    def receive(self, text_data):
        print(f"Received data: {text_data}")
        print(f"{self.channel_name} received message {text_data}")
        
        message = json.dumps(
            {
                'type': 'chat_message',
                'content': message,
                'sender': self.sender
            }
        )

        # Broadcast message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data,
                'sender': self.sender
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
