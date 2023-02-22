from rest_framework import serializers


from .models import Topic, Room, RoomComment


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


class RoomSerializer(serializers.ModelSerializer):
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


class RoomCommentSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = RoomComment
        fields = ("body",)

    def validate_body(self, value):
        print(f"body value{value}")
        if value is None or value == '':
            raise serializers.ValidationError("Comment cannot be empty")
        return value
