from django.urls import path

from . import views

urlpatterns = [
    path('rooms', views.AllRoomsView.as_view())
]