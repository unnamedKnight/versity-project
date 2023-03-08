from rest_framework import serializers
from .models import Profile


class ProfileDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email", "image_url", "github_link")

    def get_image_url(self, profile):
        request = self.context.get('request')
        image_url = profile.image.url
        return request.build_absolute_uri(image_url)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email", "image", "github_link")
        extra_kwargs = {"email": {"read_only": True}}
