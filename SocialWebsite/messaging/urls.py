from django.urls import path
from messaging import views

urlpatterns = [
    path("lobby/", views.lobby, name="lobby"),
]
