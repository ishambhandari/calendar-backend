from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer, EventsSerializer
from .tasks import send_event_notification 
from .models import Events
from django.utils import timezone
from datetime import datetime
import pytz

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        password = self.request.data.get('password')

        hashed_password = make_password(password)

        serializer.save(password=hashed_password)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token)})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



class EventsListCreateView(generics.ListCreateAPIView):
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def convert_to_utc(start_time, end_time, timezone_name):
        tz = pytz.timezone(timezone_name)
        
        # Localize the start and end times
        start_time_localized = tz.localize(start_time)
        end_time_localized = tz.localize(end_time)
        
        # Convert to UTC
        start_time_utc = start_time_localized.astimezone(pytz.utc)
        end_time_utc = end_time_localized.astimezone(pytz.utc)
        
        return start_time_utc, end_time_utc

    def get_queryset(self):
        return Events.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        start_time = self.request.data.get('start_time')
        end_time = self.request.data.get('end_time')
        timezone_name = self.request.data.get('timezone')

        # Parse start_time and end_time strings to datetime objects
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
        print('this is starttime', start_time)
        print('this is endtime', end_time)

        # Convert to UTC

        # Update serializer data with UTC times
        serializer.validated_data['start_time'] = start_time
        serializer.validated_data['end_time'] = end_time

        serializer_instance = serializer.save(created_by=self.request.user)
        user = self.request.user
        # send_event_notification.delay(serializer_instance.id,user.email)


class EventsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Events.objects.filter(created_by=self.request.user)
