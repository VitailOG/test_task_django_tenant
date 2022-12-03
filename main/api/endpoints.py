from django.db import connection, transaction
from django.db.models import Value
from rest_framework import response, status, permissions, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet

from django_tenant_test.viewsets import AppModelViewSet, SetSchemaView
from info_restaurant.models import Menu, Category, Product
from ..models import Restaurant
from ..services.create_restaurant import RestaurantCreator
from .serializers import (
    CreateRestaurantSerializer,
    MenuSerializer,
    CategorySerializer,
    ProductSerializer,
    RestaurantSerializer
)


class CreateRestaurantAPI(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateRestaurantSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data | {"owner": request.user.id})
        serializer.is_valid(raise_exception=True)
        id = RestaurantCreator(**serializer.validated_data)()
        return response.Response(
            RestaurantSerializer(serializer.validated_data | {"id": id}).data, status=status.HTTP_201_CREATED
        )


class RestaurantAPI(
    mixins.RetrieveModelMixin,
    GenericViewSet,
    SetSchemaView,
):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data | {"owner": request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        Restaurant.delete_restaurant(request.schema_name, kwargs['pk'])
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class MenusAPI(AppModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

    def get_queryset(self):
        return Menu.objects.annotate(schema=Value(self.request.schema_name))


class CategoryAPI(AppModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        return Category.objects.annotate(schema=Value(self.request.schema_name))


class ProductAPI(AppModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        return Product.objects.annotate(schema=Value(self.request.schema_name))
