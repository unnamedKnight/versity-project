from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "status": status.HTTP_403_FORBIDDEN,
                    "errors": serializer.errors,
                    "message": "Something went wrong",
                }
            )

        serializer.save()
        user = User.objects.get(email=serializer.data["email"])
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "payload": serializer.data,
                "token": str(token),
                "message": "New user created successfully",
            }
        )



class LogoutView(APIView):
    def post(self, request):
        if request.method == 'POST':
            request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)