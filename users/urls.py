from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from users.api.endpoints import RetrieveUserAPI, SignUpAPI

urlpatterns = [
    path('create-token/', ObtainAuthToken.as_view()),
    path('me/', RetrieveUserAPI.as_view()),
    path('sign-up/', SignUpAPI.as_view()),
]
