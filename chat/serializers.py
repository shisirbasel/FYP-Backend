from rest_framework import serializers
from chat.models import Message

class MessageSerializer(serializers.ModelSerializer):
    is_me = serializers.SerializerMethodField()
    class Meta:
        model= Message
        fields = ['id', 'is_me','text','created','receiver','sender']
    
    def get_is_me(self, obj):
        return self.context['user'] == obj.sender