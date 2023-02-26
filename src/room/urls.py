from django.urls import path

from . import views

urlpatterns = [
    path("search", views.RoomFilterView.as_view()),
    path("rooms", views.AllRoomsView.as_view()),
    path("create-room", views.CreateRoom.as_view()),
    path("room-detail/<pk>", views.RoomDetailView.as_view()),
    path("room-update/<pk>", views.UpdateRoomView.as_view()),
    path("room/<pk>/comment", views.RoomComments.as_view()),
    path("comment/<pk>", views.UpdateComment.as_view()),
    path('add-participant', views.AddParticipants.as_view()),
    path('all-topics', views.AllTopics.as_view()),
    path('recent-activity', views.RecentActivity.as_view()),
]
