from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        self.user = self.scope['user']
        # sender_id = self.scope['url_route']['kwargs']['sender_id']
        # receiver_id = self.scope['url_route']['kwargs']['receiver_id']

        # self.room_group_name = self.get_group_name(sender_id, receiver_id)
        self.room_group_name = 'messenger'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']

        data = {
            'type': 'chat_message',
            'sender': sender,
            'receiver': receiver,
            'message': message,
        }

        # print(data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            data
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': sender,
            'receiver': receiver,
            'message': message
        }))

    @staticmethod
    def get_group_name(sender_id, receiver_id):

        if sender_id > receiver_id:
            return '{}_{}'.format(receiver_id, sender_id)
        else:
            return '{}_{}'.format(sender_id, receiver_id)


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        self.user = self.scope['user']
        print(self.user.full_name)

        self.room_group_name = 'comment'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']

        data = {
            'type': 'chat_message',
            'message': message,
            'sender': sender
        }
        print(data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            data
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        print(event)

        print("send")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))