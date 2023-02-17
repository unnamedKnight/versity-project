from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(editable=False)
    image = models.ImageField(upload_to="images", default="default.png")
    github_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.email} -->@@--> {self.id}"
