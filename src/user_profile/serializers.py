from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email", "image", "github_link")
        extra_kwargs = {"email": {"read_only": True}}
