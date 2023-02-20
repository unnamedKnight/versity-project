from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .models import Topic, Room, RoomComment
from .serializers import RoomSerializer, RoomCommentSerializer
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from django.db.models import Q


User = get_user_model()

# Create your views here.


class RoomFilterView(ListModelMixin, GenericAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["topic", "name"]
    # search_fields = ["topic", "name"]

    def get(self, request, *args, **kwargs):
        if topic := request.query_params.get("topic", None):
            rooms = Room.objects.filter(topic__name__icontains=topic).order_by(
                "-created"
            )
        elif name := request.query_params.get("name", None):
            rooms = Room.objects.filter(name__icontains=name).order_by("-created")
        elif query_params := request.query_params.get("search"):
            rooms = Room.objects.filter(
                Q(name__icontains=query_params) | Q(name__icontains=query_params)
            ).order_by("-created")
        else:
            rooms = Room.objects.all().order_by("-created")
        serializer = RoomSerializer(rooms, many=True)
        return Response(data=serializer.data)

    # mark: another implementation of the code above
    # mark:the quality of the code above is better

    # def get(self, request, *args, **kwargs):
    #     if topic := request.query_params.get('topic', None):
    #         print(topic)
    #         rooms = Room.objects.filter(topic__name__icontains=topic)
    #         serializer = RoomSerializer(rooms, many=True)
    #         return Response(data=serializer.data)
    #     elif name:= request.query_params.get('name', None):
    #         rooms = Room.objects.filter(name__icontains=name)
    #         serializer = RoomSerializer(rooms, many=True)
    #         return Response(data=serializer.data)
    #     else:
    #         query_params = request.query_params.get("search")
    #         rooms = Room.objects.filter(Q(name__icontains=query_params)|
    #                                     Q(name__icontains=query_params))
    #         serializer = RoomSerializer(rooms, many=True)
    #         return Response(data=serializer.data)

    #     return self.list(request, *args, **kwargs)


class AllRoomsView(APIView):
    """
    List all rooms, or create a new room.
    """

    def get(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data})


class CreateRoom(APIView):
    permission_classes = [IsAuthenticated]

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

    permission_classes = [IsAuthenticated]

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


class RoomComments(APIView):
    """
    List all comments of a room
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        room = Room.objects.get(pk=pk)
        if not room:
            return Response({"status": status.HTTP_400_BAD_REQUEST})
        comments = RoomComment.objects.filter(room=room)
        serializer = RoomSerializer(comments, many=True)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data})

    # decorator doesn't work with APIView methods
    # @permission_classes([IsAuthenticated])
    def post(self, request, pk, format=None):
        serializer = RoomCommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"Status": status.HTTP_400_BAD_REQUEST})
        serializer.save(room=Room.objects.get(pk=pk), user=request.user)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data})


class UpdateComment(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        comment = RoomComment.objects.get(id=pk)
        if comment.user != request.user:
            return Response(
                {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "You do not have permission to perform this action",
                }
            )
        serializer = RoomCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "data": serializer.data,
                    "message": "Comment updated successfully",
                }
            )

        return Response({"Status": status.HTTP_400_BAD_REQUEST})
