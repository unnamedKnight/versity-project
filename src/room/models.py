from django.db import models

from django.contrib.auth import get_user_model

from user_profile.models import Profile

# Create your models here.


class TopicField(models.CharField):
    """
    This class will turn topic name into lower case before saving
    """

    def get_prep_value(self, value):
        return str(value).strip().lower()


class Topic(models.Model):
    name = TopicField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(Profile, related_name="host", on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, related_name="topic", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(Profile, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return f"{self.name} --> {self.id}"


class RoomComment(models.Model):
    comment_owner = models.ForeignKey(Profile, related_name="comment_owner", on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return f"{self.id}"
