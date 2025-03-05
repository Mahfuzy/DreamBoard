from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class GroupChatConsumer(WebsocketConsumer):
    """
    WebSocket consumer for handling group chat functionality.

    - Users connect to a chat room based on `room_name` in the URL.
    - Messages are broadcast to all users in the room.
    - Users automatically join and leave chat groups upon connection and disconnection.

    Methods:
        - connect(): Joins the WebSocket to a room group.
        - disconnect(): Removes the WebSocket from the room group.
        - receive(): Broadcasts incoming messages to the group.
        - chat_message(): Sends messages received from the group to the WebSocket.
    """

    def connect(self):
        """Handles WebSocket connection and joins the chat room."""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print(f"WebSocket connected to room {self.room_name}")

    def disconnect(self, close_code):
        """Handles WebSocket disconnection and removes it from the chat room."""
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected from room {self.room_name}")

    def receive(self, text_data):
        """Receives a message and broadcasts it to the chat room."""
        print(f"Received data: {text_data}")

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data
            }
        )

    def chat_message(self, event):
        """Sends a message from the chat room to the WebSocket."""
        message = event['message']
        self.send(text_data=message)


class DirectChatConsumer(WebsocketConsumer):
    """
    WebSocket consumer for handling direct messages between users.

    - Users connect to a chat room identified by sender and recipient usernames.
    - Messages are broadcast only to the specific recipient.
    - Users automatically join and leave private chat groups.

    Methods:
        - connect(): Joins the WebSocket to a private chat room.
        - disconnect(): Removes the WebSocket from the private chat room.
        - receive(): Broadcasts direct messages.
        - chat_message(): Sends messages received from the private chat to the WebSocket.
    """

    def connect(self):
        """Handles WebSocket connection and joins the private chat room."""
        self.sender = self.scope['user'].username
        self.recipient = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'direct_{self.sender}_{self.recipient}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print(f"WebSocket connected to room {self.room_group_name}")

    def disconnect(self, close_code):
        """Handles WebSocket disconnection and removes it from the private chat room."""
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected from room {self.room_group_name}")

    def receive(self, text_data):
        """Receives a message and sends it to the recipient."""
        print(f"Received data: {text_data}")

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data,
                'sender': self.sender
            }
        )

    def chat_message(self, event):
        """Sends a direct message from the chat room to the WebSocket."""
        message = event['message']
        sender = event['sender']

        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
