# Generated by Django 4.1.7 on 2023-02-17 16:30

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=255, null=True)),
                ("last_name", models.CharField(blank=True, max_length=255, null=True)),
                ("email", models.EmailField(max_length=254)),
                ("image", models.ImageField(default="default.png", upload_to="images")),
                ("github_link", models.URLField(blank=True, null=True)),
            ],
        ),
    ]