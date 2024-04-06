from rest_framework import serializers
from .models import chatMsg

class chatMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = chatMsg
        fields = ["sender", "message"]