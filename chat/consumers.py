from channels.generic.websocket import WebsocketConsumer
import json
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("WebSocket connected")

    def disconnect(self, close_code):
        print(f"WebSocket disconnected with code {close_code}")

    def receive(self, text_data):
        print(f"Received data: {text_data}")
        # Process the received data and send a response
        self.send(f"{text_data} is what you sent")
        
        
    
    
