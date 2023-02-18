from rest_framework import serializers


from .models import Topic, Room, RoomComment

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class RoomCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomComment
        fields = "__all__"


