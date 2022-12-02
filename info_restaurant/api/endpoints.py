from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from main.api.serializers import ProductSerializer
from .serializers import RetrieveMenuSerializer, RetrieveCategorySerializer
from ..models import Menu, Category, Product


class RetrieveMenuAPI(
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Menu.objects.prefetch_related('categories').all()
    serializer_class = RetrieveMenuSerializer


class RetrieveCategoryAPI(
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = RetrieveCategorySerializer


class RetrieveProductAPI(
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
