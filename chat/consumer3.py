from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from accounts.models import User
from .models import Message, Conversation


class ChatConsumer(WebsocketConsumer):

    def new_message(self, data):
        message = data.get('message', None)
        key = data.get('conversation_key', None)

        sender = message['sender']
        receiver = message['receiver']

        sender = User.objects.get(id=sender['id'])
        receiver = User.objects.get(id=receiver['id'])

        conversation, created = Conversation.objects.get_or_create(key=key)
        Message.objects.create(conversation=conversation, sender=sender,
                                         receiver=receiver, content=message['content'])

        content = {
            'command': 'new_message',
            'conversation_key': key,
            'message': message
        }
        self.send_chat_message(content)



    commands = {
        # 'init_chat': init_chat,
        # 'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    """ ==================== Main Methods Start ======================== """

    def connect(self):
        self.room_name = 'hello'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # leave group room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)

        print(data)

        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    """ ==================== Main Methods End ========================"""

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    def messages_to_json(self, messages):
        result = []

        for message in messages:
            result.append(self.message_to_json(message))

        return result

    def message_to_json(self, message):
        return {
            'sender': message.sender.username,
            'content': message.content,
            'created_at': str(message.created_at)
        }


    @staticmethod
    def get_conversation_key(sender_id, receiver_id):

        if int(sender_id) < int(receiver_id):
            return "{}_{}".format(sender_id, receiver_id)

        return "{}_{}".format(sender_id, receiver_id)

    # def init_chat(self, data):
    #     username = data['username']
    #     user, created = User.objects.get_or_create(username=username)
    #
    #     content = {
    #         'command': 'init_chat'
    #     }
    #
    #     if not user:
    #         content['error'] = 'Unable to get or create User with username: ' + username
    #         self.send_message(content)
    #
    #     content['success'] = 'Chatting in with success with username: ' + username
    #     self.send_message(content)
    #
    # def fetch_messages(self, data):
    #     messages = Message.objects.last_50_messages()
    #
    #     content = {
    #         'command': 'messages',
    #         'messages': self.messages_to_json(messages)
    #     }
    #     self.send_message(content)
