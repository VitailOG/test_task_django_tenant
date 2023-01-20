from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django_tenant_test.serializers import Serializer
from users.models import CustomUserProfile


class RetrieveUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    date_joined = serializers.SerializerMethodField()

    def get_date_joined(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d %H:%M:%S")


class SignUpSerializer(Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUserProfile.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    class Meta:
        exclude_fields = ["password2"]
