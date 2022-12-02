from rest_framework import serializers

from info_restaurant.models import Menu, Category
from main.api.serializers import CategorySerializer, ProductSerializer


class RetrieveMenuSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Menu
        fields = ("id", "restaurant", "type", "categories")


class RetrieveCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "menu", "name", "products")
