from django.urls import path

from . import views

urlpatterns = [
    path('rooms', views.AllRoomsView.as_view()),
    path('room-detail/<pk>', views.RoomDetailView.as_view()),
    path('room-update/<pk>', views.UpdateRoomView.as_view())
]