from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from info_restaurant.models import Menu, Category, Product
from main.models import Restaurant


User = get_user_model()


class CreateRestaurantSerializer(serializers.Serializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), validators=[UniqueValidator(queryset=Restaurant.objects.all())]
    )
    name = serializers.CharField(label='Назва ресторана', max_length=256)
    address = serializers.CharField(label='Адрес ресторана', max_length=256)


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            "id",
            "schema_name",
            "created",
            "modified",
            "name",
            "address",
            "owner",
        )
        read_only_fields = ("schema_name",)


class MenuSerializer(serializers.ModelSerializer):
    schema = serializers.CharField(read_only=True)
    # restaurant = serializers.PrimaryKeyRelatedField()  # todo test

    class Meta:
        model = Menu
        fields = ("id", "restaurant_id", "type", "schema")


class CategorySerializer(serializers.ModelSerializer):
    schema = serializers.CharField(read_only=True)
    # menu_id = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Category
        fields = ("id", "menu_id", "name", "schema")


class ProductSerializer(serializers.ModelSerializer):
    schema = serializers.CharField(read_only=True)
    # category_id = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Product
        fields = ("id", "category_id", "name", "price", "schema")
