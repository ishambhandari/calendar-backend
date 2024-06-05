from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Events

from django.db.models import Q
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

        if start_time and end_time:
            # Filter overlapping events for the same user
            user_id = self.context['request'].user.id
            overlapping_events = Events.objects.filter(
                Q(start_time__lt=end_time, end_time__gt=start_time) &
                (Q(created_by=user_id) | Q(created_by__isnull=True))
            )
            
            if self.instance:
                overlapping_events = overlapping_events.exclude(id=self.instance.id)
                
            if overlapping_events.exists():
                raise serializers.ValidationError("The event overlaps with existing events.")

        return data
