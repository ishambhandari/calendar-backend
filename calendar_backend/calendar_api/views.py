from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer, EventsSerializer
from .models import Events

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        # Extract password from request data
        password = self.request.data.get('password')

        # Hash the password
        hashed_password = make_password(password)

        # Set the hashed password in the serializer
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

    def get_queryset(self):
        return Events.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EventsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Events.objects.filter(created_by=self.request.user)
