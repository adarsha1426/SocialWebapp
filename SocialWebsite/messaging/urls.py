from django.urls import path
from messaging import views
from . import consumers

urlpatterns = [
    path("lobby/", views.lobby, name="lobby"),
    path("ws/chat/", consumers.ChatConsumer.as_asgi()),
]
