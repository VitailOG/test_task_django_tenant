from rest_framework import response, permissions, views, status

from ..models import CustomUserProfile
from .serializers import RetrieveUserSerializer, SignUpSerializer


class RetrieveUserAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return response.Response(
            RetrieveUserSerializer(request.user).data, status=status.HTTP_200_OK
        )


class SignUpAPI(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CustomUserProfile.objects.create_user(**serializer.validated_data)
        return response.Response(
            {"created": True}, status=status.HTTP_201_CREATED
        )
