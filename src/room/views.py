from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Topic, Room, RoomComment
from .serializers import RoomSerializer, RoomCommentSerializer


User = get_user_model()

# Create your views here.


class AllRoomsView(APIView):
    """
    List all rooms, or create a new room.
    """

    def get(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data})

    def post(self, request, format=None):
        serializer = RoomSerializer(data=request.data)
        topic = request.data.get("topic").strip()
        if topic is None:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Please provide a value for topic",
                }
            )
        # --------------------- working part --------------------- #
        # we are getting or creating a new topic_obj
        # then assigning serializer_initial data with that value
        topic_obj, _ = Topic.objects.get_or_create(
            defaults={"name": topic}, name__iexact=topic
        )
        serializer.initial_data._mutable = True
        serializer.initial_data["topic"] = topic_obj.id
        serializer.initial_data._mutable = False

        # -------------------------- end ------------------------- #
        if serializer.is_valid():
            serializer.save(host=request.user)
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    "message": "New Room created successfully",
                    "data": serializer.data,
                }
            )
        return Response(
            {"status": status.HTTP_400_BAD_REQUEST, "error": serializer.errors}
        )


class RoomDetailView(APIView):
    """
    Returns the details of a Room instance
    """

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, pk, format=None):
        room = self.get_object(pk)
        serializer = RoomSerializer(room)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data})


class UpdateRoomView(APIView):
    """
    Update a room instance
    """

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist as e:
            raise Http404 from e

    def put(self, request, pk, format=None):
        room = self.get_object(pk)
        if room.host != request.user:
            return Response(
                {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "You do not have permission to perform this action",
                }
            )
        serializer = RoomSerializer(room, data=request.data)
        topic = request.data.get("topic").strip()
        if topic is None:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "error": {"topic": ["This field is required"]},
                    "message": "Please provide a value for topic",
                }
            )
        # --------------------- working part --------------------- #
        # we are getting or creating a new topic_obj
        # then assigning serializer_initial data with that value
        topic_obj, _ = Topic.objects.get_or_create(
            defaults={"name": topic}, name__iexact=topic
        )
        serializer.initial_data._mutable = True
        serializer.initial_data["topic"] = topic_obj.id
        serializer.initial_data._mutable = False

        # -------------------------- end ------------------------- #

        if serializer.is_valid():
            serializer.save(host=request.user)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Room updated successfully",
                    "data": serializer.data,
                }
            )
        return Response(
            {"status": status.HTTP_400_BAD_REQUEST, "error": serializer.errors}
        )
