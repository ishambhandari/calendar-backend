from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Events
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'email']


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'created_by', 'title', 'description', 'start_time', 'end_time']
        read_only_fields = ['created_by']

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if end_time and start_time and end_time <= start_time:
            raise serializers.ValidationError("end_time must be after start_time")
        return data
