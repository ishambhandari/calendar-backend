
from django.contrib import admin
from django.urls import path, include
from .views import SignupView, LoginView, EventsListCreateView, EventsRetrieveUpdateDestroyView

urlpatterns = [
    path('signup/', SignupView.as_view(), name = 'signup'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('event/', EventsListCreateView.as_view(), name = 'event'),
    path('event/<int:pk>/', EventsRetrieveUpdateDestroyView.as_view(), name='event-detail'),
    path('alter_event/', EventsRetrieveUpdateDestroyView.as_view(), name = 'alter_event'),

]
