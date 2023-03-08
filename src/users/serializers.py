from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=155, required=True)
    last_name = serializers.CharField(max_length=155, required=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
        }

    def save(self):
        password = self.validated_data["password"]
        password2 = self.validated_data.pop("password2")

        first_name = self.validated_data.get("first_name", None)
        if first_name is None:
            raise serializers.ValidationError({"error": "First name must be provided"})

        last_name = self.validated_data.get("last_name", None)
        if last_name is None:
            raise serializers.ValidationError({"error": "Last name must be provided"})

        if password != password2:
            raise serializers.ValidationError(
                {"error": "Password1 and Password2 should be same!"}
            )

        if User.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "Email already exists!"})

        account = self.validated_data
        account = User(account)
        errors = {}
        try:
            validate_password(password=password, user=account)

        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        account = User(email=self.validated_data["email"])
        account.set_password(password)
        account.save()

        return account
