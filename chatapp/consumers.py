from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.user_name = self.scope["user"].username

        if self.scope["user"].is_anonymous:
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


    async def receive_json(self, text_data):
        """
        Runs when client executes "socket.send" to send some data to webSocket server.
        """
        print(text_data)
        load_message = json.loads(text_data)
        print(load_message)
        message = load_message["message"]
        command = load_message["command"]
        print('\n', 'message is: ', message, '\n')
        print('\n', 'command is: ', command, '\n')
        if(command == "send"):
            await self.channel_layer.group_send(
            "list",
            {
                "type": "chat.send",
                "username": self.user_name,
                "message": message,
            })

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

    async def chat_end(self, event):
        """
        Called at the end of user's connection to webSocket.
        """

        # Send a message down to the client
        await self.send_json(
            {
                "username": event["username"],
                "is_logged_in": event["is_logged_in"],
            },
        )

    async def chat_send(self, event):
        """
        Called when user sends a message to a group.
        """

        # Send a message down to the client
        await self.send_json(
            {
                "echo_to_client": True,
                "username": event["username"],
                "message": event["message"],
            },
        )