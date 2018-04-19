from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
# from channels.auth import login, logout

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user_name = self.scope['session']['user']['username']

        # async_to_sync(login)(self.scope, user)
        # self.scope["session"].save()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            "list",
            self.channel_name
        )

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            "list",
            {
                'username': self.user_name,
                'is_logged_in': True
            }
        )

        self.accept()

    def disconnect(self, close_code):
        self.user_name = self.scope['session']['user']['username']

        # async_to_sync(logout)(self.scope)
        # self.scope["session"].save()

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            "list",
            self.channel_name
        )

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            "list",
            {
                'username': self.user_name,
                'is_logged_in': True
            }
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            "list",
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

