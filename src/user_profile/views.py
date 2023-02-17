from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ProfileSerializer
from .models import Profile

# Create your views here.


class ProfileDetailView(APIView):
    def get_object(self, pk):
        """
        Get Profile instance with given pk
        """

        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, pk, format=None):
        """Get user Profile information with given pk"""

        # if request.auth.key:
        #     print(f"user auth key: {request.auth.key}")
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(
            {
                "status": status.HTTP_200_OK,
                "data": serializer.data,
            }
        )


# class CreateProfile(APIView):

#     """
#     List all Profiles, or create a new Profile.
#     """

#     # parser_classes = (MultiPartParser,)

#     def post(self, request, format=None):
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     "status": status.HTTP_201_CREATED,
#                     "message": "Profile created successfully",
#                     "data": serializer.data,
#                 }
#             )
#         return Response(
#             {
#                 "status": status.HTTP_400_BAD_REQUEST,
#                 "message": "something went wrong",
#                 "errors": serializer.errors,
#             }
#         )


class UpdateProfile(APIView):

    """
    Retrieve, update or delete a Profile instance.
    """

    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Get Profile instance with given pk
        """

        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist as e:
            raise Http404 from e

    def put(self, request, pk, format=None):
        """
        Update a Profile with the given pk
        """

        profile = self.get_object(pk)

        # checking if profile owner is the authenticated user
        if profile.user != request.user:
            return Response(
                {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "You Don't have permission to perform this action",
                }
            )

        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            # saving the foreign key field while saving the serializer
            serializer.save(user=profile.user)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Profile updated successfully",
                    "data": serializer.data,
                }
            )
        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "something went wrong",
                "errors": serializer.errors,
            }
        )
