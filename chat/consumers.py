from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from django.db.models import Q
from core.models import TradeRequest, User
from chat.models import Message
from chat.serializers import MessageSerializer
from core.serializers import ProfileSerializer
class ChatConsumer(WebsocketConsumer):

    def connect(self):
        user = self.scope['user']
        if not user.is_authenticated:
            return
        self.username = user.username

        #Join this user to a group with their username
        async_to_sync(self.channel_layer.group_add)(
            self.username, self.channel_name
        )
        self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.username, self.channel_name
        )
    
    #------------------------------------------
    #-------handle requests-------------------
    #------------------------------------------
        
    def receive(self, text_data):

        data = json.loads(text_data)
        data_source = data.get('source')

        print('receive', json.dumps(data, indent=2))

        if data_source == "message.send":
            self.receive_message_send(data)
        
        elif data_source == "message.list":
            self.receive_message_list(data)

    

    def receive_message_send(self, data):
        user = self.scope['user']
        id = data.get('id')
        message_text = data.get('message')
        requested_user = User.objects.get(id=id)

        try:
            traderequest = TradeRequest.objects.filter(Q(user=user) | Q(user=requested_user), Q(requested_book__user=user) | Q(requested_book__user=requested_user)).first()

        except TradeRequest.DoesNotExist:
            print("Error: Could not find any traderequest")
            return

        message = Message.objects.create(
            trade_request=traderequest,
            sender=user,
            text=message_text,
            receiver=requested_user
        )

        # Serialize message and friend
        serialized_message = MessageSerializer(
            message,
            context={'user': user}
        ).data

        serialized_friend = ProfileSerializer(requested_user).data

        data = {
            'message': serialized_message,
            'friend': serialized_friend
        }

        self.send_group(user.username, 'message.send', data)

        # Send new message to receiver
        serialized_message = MessageSerializer(
            message,
            context={'user': requested_user}
        ).data

        serialized_user = ProfileSerializer(user).data
        data = {
            'message': serialized_message,  
            'friend': serialized_user
        }
        self.send_group(requested_user.username, 'message.send', data)


    def receive_message_list(self, data):
        user = self.scope['user']
        id = data.get('id')
        print(id)
        try:
            requested_user = User.objects.get(id=id)
        except User.DoesNotExist:
            print("Error: User with id {} does not exist".format(id))
            return
        
        try:
            traderequest = TradeRequest.objects.filter(Q(user = user) | Q(user = requested_user) , Q(requested_book__user = user ) | Q(requested_book__user = requested_user)).first()

        except TradeRequest.DoesNotExist:
            print("Error: Could not find any traderequest")
            return 

        #get messages
        messages = Message.objects.filter(
            Q (sender = user,
            receiver = requested_user) | Q(sender = requested_user,
            receiver = user),
            trade_request = traderequest
        ).order_by ('-created')
        print(messages)
        serialized_message = MessageSerializer(
                messages,
                many=True,
                context={'user': user} 
            )

        serialized_friend = ProfileSerializer(requested_user)

        data = {
            'messages': serialized_message.data,
            'friend': serialized_friend.data
        }

        #send back to request
        self.send_group(user.username, 'message.list', data)

    
    def send_group(self, group, source, data):
        response = {
            'type' : 'broadcast_group',
            'source' : source,
            'data': data
        }

        async_to_sync(self.channel_layer.group_send)(
            group, response
        )
    
    def broadcast_group(self, data):
        self.send(text_data=json.dumps(data) )