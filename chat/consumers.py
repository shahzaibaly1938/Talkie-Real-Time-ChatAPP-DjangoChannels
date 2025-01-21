import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .templatetags.chatextras import initials

from accounts.models import User

from .models import Message, Room

from django.utils.timesince import timesince

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        # Join the Room Group
        await self.get_room()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f"Connected to room: {self.room_name}")  # Debug log

        #Inform User
        if self.user.is_staff:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'users_update'
                }
            )

    async def disconnect(self, close_code):
        # Leave Room
        print(f"Disconnected from room: {self.room_name}")  # Debug log
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if not self.user.is_staff:
            await self.set_room_closed()
    
    
    async def receive(self, text_data):
        # recieve messages from websocket frontend
        print(f"Message received: {text_data}")  # Debug log

        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        name = text_data_json['name']
        agent = text_data_json.get('agent', '')

        print('Receive: ',type)

        if type == 'message':
            new_message = await self.create_message(name, message, agent)

            # Send Message to Group / Room
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type':'chat_message',
                    'message':message,
                    'name':name,
                    'agent':agent,
                    'initials':initials(name),
                    'created_at': timesince(new_message.created_at),
                }
            )
            print(f"Message sent to group: {self.room_group_name}")
        
        elif type == 'update':
            #Send Update to th Room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'writing_active',
                    'message':message,
                    'name':name,
                    'agent':agent,
                    'initials':initials(name),
                }
            )

        else:
            print(f'message type: {type}')

    async def chat_message(self, event):
        # Sent message to WeSocket (frontend)

        print(f"Broadcasting message: {event['message']}")  # Debug log

        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message' : event['message'],
            'name' : event['name'],
            'agent' : event['agent'],
            'initials' : event['initials'],
            'created_at' : event['created_at'],
        }))

    async def writing_active(self, event):
        #Send writing is active to room
        await self.send(text_data=json.dumps(
            {
            'type': event['type'],
            'message' : event['message'],
            'name' : event['name'],
            'agent' : event['agent'],
            'initials' : event['initials'],   
            }
        ))



    async def users_update(self, event):
        #Send information to the WebSocket
        await self.send(text_data=json.dumps(
            {
                'type':'users_update'
            }
        ))
    



    @sync_to_async
    def get_room(self):
        self.room = Room.objects.get(uuid=self.room_name)

    @sync_to_async
    def set_room_closed(self):
        self.room.status = Room.CLOSED
        self.room.save()
        print('room closed')

    @sync_to_async
    def create_message(self, sent_by, message, agent):
        message = Message.objects.create(body=message, sent_by=sent_by)

        if agent:
            message.created_by = User.objects.get(pk=agent)
            message.save()

        self.room.messages.add(message)

        return message