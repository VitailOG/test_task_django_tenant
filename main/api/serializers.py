from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
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


class CustomPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        if not isinstance(data, int):
            assert "type_error" in self.error_messages, "Add to error_messages key type_error"
            self.fail('type_error', pk_value=data)
        try:
            return self.get_queryset().get(id=data).id
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)


class MenuSerializer(serializers.ModelSerializer):
    schema = serializers.CharField(read_only=True)
    restaurant_id = CustomPrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(), error_messages={"type_error": "Type must be int"}
    )

    class Meta:
        model = Menu
        fields = ("id", "restaurant_id", "type", "schema")


class CategorySerializer(serializers.ModelSerializer):
    schema = serializers.CharField(read_only=True)
    menu_id = CustomPrimaryKeyRelatedField(
        queryset=Menu.objects.all(), error_messages={"type_error": "Type must be int"}
    )

    class Meta:
        model = Category
        fields = ("id", "menu_id", "name", "schema")


class ProductSerializer(serializers.ModelSerializer):
    schema = serializers.CharField(read_only=True)
    category_id = CustomPrimaryKeyRelatedField(
        queryset=Category.objects.all(), error_messages={"type_error": "Type must be int"}
    )

    class Meta:
        model = Product
        fields = ("id", "category_id", "name", "price", "schema")
