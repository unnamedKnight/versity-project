from rest_framework import serializers
from .models import Profile
from room.serializers import RoomSerializer


class ProfileDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    rooms = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "image_url",
            "github_link",
            "rooms",
        )
        extra_kwargs = {
            "id": {
                "read_only": True,
            }
        }

    def get_image_url(self, profile):
        request = self.context.get("request")
        image_url = profile.image.url
        return request.build_absolute_uri(image_url)

    def get_rooms(self, profile):
        request = self.context.get("request")
        rooms = profile.host.all()
        return RoomSerializer(
            rooms, many=True, read_only=True, context={"request": request}
        ).data


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email", "image", "github_link")
        extra_kwargs = {"email": {"read_only": True}}
