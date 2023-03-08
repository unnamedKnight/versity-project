from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
import threading
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from user_profile.models import Profile


User = get_user_model()


# class EmailThread(threading.Thread):
#     """Using threading for sending email faster"""

#     def __init__(self, email) -> None:
#         self.email = email
#         threading.Thread.__init__(self)

#     def run(self) -> None:
#         self.email.send()


class RegisterUser(APIView):
    def post(self, request):

        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

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

        # ------------------- confirmation mail ------------------ #

        # user_email = user.email
        # uid = urlsafe_base64_encode(force_bytes(user.pk))
        # current_site = get_current_site(request)
        # confirmation_token = default_token_generator.make_token(user)
        # link = reverse(
        #     "activate",
        #     kwargs={"uidb64": uid, "token": confirmation_token},
        # )

        # activate_url = f"http://{current_site.domain}{link}"
        # email_body = (
        #     "Hi "
        #     + user_email
        #     + f", We just need to verify your email address before you can access {current_site.domain}\n"
        #     + f"Verify your email address: {activate_url} \n"
        #     + "Thanks! – The Out of Business team"
        # )

        # email_subject = "Activate Your Account"
        # email = EmailMessage(
        #     email_subject,
        #     email_body,
        #     # sender
        #     "forangela100@gmail.com",
        #     # receivers
        #     [user_email],
        # )
        # # email.send(fail_silently=False)

        # EmailThread(email).start()

        # -------------------------- end ------------------------- #

        # --------------- create a profile Instance -------------- #

        user_profile = Profile.objects.create(
            user=user, first_name=first_name, last_name=last_name, email=user.email
        )
        user_profile.save()

        # -------------------------- end ------------------------- #

        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "payload": serializer.data,
                "token": str(token),
                "message": "New user created successfully",
            }
        )


# class Activate(APIView):
#     def get(self, request, uidb64, token):
#         try:
#             user_id = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=user_id)
#         except (
#             TypeError,
#             ValueError,
#             OverflowError,
#             User.DoesNotExist,
#             DjangoUnicodeDecodeError,
#         ):
#             user = None
#         if user is None:
#             return Response(
#                 {"status": status.HTTP_400_BAD_REQUEST, "message": "User not found"}
#             )
#         if user.is_verified:
#             return Response(
#                 {
#                     "status": status.HTTP_400_BAD_REQUEST,
#                     "message": "Email has already been verified.",
#                 }
#             )

#         if not default_token_generator.check_token(user, token):
#             return Response(
#                 {
#                     "status": status.HTTP_400_BAD_REQUEST,
#                     "message": "Token is invalid or expired. Please request \
# another confirmation email by signing in.",
#                 }
#             )
#         user.is_verified = True
#         user.save()
#         return Response(
#             {
#                 "status": status.HTTP_200_OK,
#                 "message": "Email Successfully Confirmed",
#             }
#         )


class CustomAuthToken(ObtainAuthToken):
    """Returns  a token to a verified user. Equivalent to loginview"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        profile = Profile.objects.get(user=user)
        # if not user.is_verified:
        #     return Response(
        #         {
        #             "status": status.HTTP_401_UNAUTHORIZED,
        #             "message": "Please Verify Your Email.",
        #         }
        #     )
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": str(token),
                "user_id": user.pk,
                "email": user.email,
                "profile_id": profile.id,
            }
        )


class LogoutView(APIView):
    def post(self, request):
        if request.method == "POST":
            request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
