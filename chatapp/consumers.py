from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.user_name = self.scope["user"].username

        if self.scope["user"].is_anonymous:
            print("anonymous")
            await self.close()
        else:
            # Join room group
            await self.channel_layer.group_add(
                "list",
                self.channel_name
            )

            # Sends JSON to the group
            await self.channel_layer.group_send(
                "list",
                {
                    "type": "chat.start",
                    "username": self.user_name,
                    "is_logged_in": True,
                }
            )

            # For accepting the connection
            await self.accept()

            # Tell client to execute "connect" code
            await self.send_json({
                "connect": True,
            })

            


    async def disconnect(self, close_code):
        """
        Called when the user's connection to WebSocket closes.
        """

        self.user_name = self.scope["user"].username

        # Sends JSON to the group
        await self.channel_layer.group_send(
            "list",
            {
                "type": "chat.end",
                "username": self.user_name,
                "is_logged_in": False,
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(
            "list",
            self.channel_name,
        )

        # Tell client to execute "disconnect" code
        await self.send_json({
            "connect": False,
        })


    async def receive_json(self, text_data):
        """
        Runs when client executes "socket.send" to send some data to webSocket server.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            "list",
            {
                "type": "chat.message",
                "message": message,
                "username": self.scope["user"].username,
            }
        )

    # Receive message from room group
    # def chat_message(self, event):
    #     message = event['message']

    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps({
    #         "message": message
    #     }))


    # GROUP SEND HANDLERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    async def chat_start(self, event):
        """
        Called at the start of user's connection to webSocket.
        """

        # Send a message down to the client
        await self.send_json(
            {
                "username": event["username"],
                "is_logged_in": event["is_logged_in"],
            },
        )
