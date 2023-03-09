from rest_framework import serializers


from .models import Topic, Room, RoomComment
from user_profile.models import Profile


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"

    # def _get_or_create_topic(self, topic):
    #     """Handle getting or creating topic as needed."""
    #     topic_obj, created = Topic.objects.get_or_create(
    #         defaults={"name": topic["name"]}, title__iexact=topic["name"]
    #     )
    #     return topic_obj

    # def create(self, validated_data):
    #     """Create a topic or get an existing topic"""
    #     # removing tag from validated data
    #     topic = validated_data.pop("name", None)
    #     topic_obj = self._get_or_create_topic(self, topic.lower())
    #     return topic_obj

    # def update(self, instance, validated_data):
    #     """Update a topic"""
    #     topic = validated_data.pop("name", None)
    #     instance.name = self._get_or_create_topic(topic.lower())
    #     instance.save()
    #     return instance


class ProfileSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("id", "first_name", "last_name", "email", "image_url", "github_link")

    def get_image_url(self, instance):
        request = self.context.get("request")
        image_url = instance.image.url
        return request.build_absolute_uri(image_url)



class RoomSerializer(serializers.ModelSerializer):
    host = ProfileSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ("id", "host", "topic", "name", "description")


class CommentSerializer(serializers.ModelSerializer):
    comment_owner = ProfileSerializer(read_only=True)

    class Meta:
        model = RoomComment
        fields = ("id", "room", "comment_owner", "body", "created")
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "room": {
                "read_only": True,
            },
            "created": {
                "read_only": True,
            },
        }


class RoomFilterSerializer(serializers.ModelSerializer):
    host = ProfileSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    participants = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "id",
            "host",
            "topic",
            "name",
            "description",
            "participants",
            "comments",
        )


# -- Adding CommentSerializer and ProfileSerializer for RoomDetailSerializer - #


class RoomDetailSerializer(serializers.ModelSerializer):
    host = ProfileSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    participants = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "id",
            "host",
            "topic",
            "name",
            "description",
            "participants",
            "comments",
        )


# ------------------------- RoomDetailSerializer End ------------------------- #


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("topic", "name", "description")
        # extra_kwargs = {"topic": {"read_only": True}}

    # def _get_or_create_topic(self, topic):
    #     """Handle getting or creating topic as needed."""
    #     topic_obj, created = Topic.objects.get_or_create(
    #         defaults={"name": topic}, name__iexact=topic
    #     )
    #     return topic_obj.id

    # def validate_topic(self, value):
    #     if not value:
    #         raise serializers.ValidationError('Please provide a Topic name.')
    #     return self._get_or_create_topic(value)

    # def create(self, validated_data):
    #     """Create a Room"""

    #     topic = validated_data.pop('topic')
    #     topic_instance, created = Topic.objects.get_or_create(name=topic)
    #     room = Room.objects.create(**validated_data, topic=topic_instance)
    #     room.save()
    #     return room

    # def update(self, instance, validated_data):
    #     """Update Room."""
    #     topic = validated_data.pop("topic", None)
    #     clean_topic, _ = Topic.objects.get_or_create(name=topic)
    #     instance.topic = clean_topic
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance


# class UpdateRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = ("id", "topic", "name", "description")
#         extra_kwargs = {"id": {"read_only": True}}


class RoomCommentDetailSerializer(serializers.ModelSerializer):
    comment_owner = ProfileSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = RoomComment
        fields = ("id", "comment_owner", "room", "body", "created")
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "created": {
                "read_only": True,
            },
        }


class RoomCommentSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = RoomComment
        fields = ("body",)

    def validate_body(self, value):
        constrain1 = '""'
        constrain2 = "''"
        splitted_value = value.split()
        check_value = "".join(splitted_value)

        if (
            value is None
            or value == constrain1
            or value == constrain2
            or len(splitted_value) == 0
            or check_value == constrain1
            or check_value == constrain2
        ):
            raise serializers.ValidationError("Comment cannot be empty")
        return value
