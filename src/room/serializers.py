from rest_framework import serializers


from .models import Topic, Room, RoomComment


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"

    def _get_or_create_topic(self, topic):
        """Handle getting or creating topic as needed."""
        topic_obj, created = Topic.objects.get_or_create(
            defaults={"name": topic["name"]}, title__iexact=topic["name"]
        )
        return topic_obj.lower()

    def create(self, validated_data):
        """Create a topic or get an existing topic"""
        # removing tag from validated data
        topic = validated_data.pop("name", None)
        filtered_topic = self._get_or_create_topic(self, topic.lower())
        topic = Topic.objects.create(name=filtered_topic)
        return topic


    def update(self, instance, validated_data):
        """Update a topic"""
        topic = validated_data.pop("name", None)
        instance.name = self._get_or_create_topic(topic.lower())
        instance.save()
        return instance


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("topic", "name", "description")


class RoomCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomComment
        fields = ("body",)
