from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from main.api.serializers import ProductSerializer
from .serializers import RetrieveMenuSerializer, RetrieveCategorySerializer
from .. import models


class RetrieveMenuAPI(RetrieveModelMixin, GenericViewSet):
    queryset = models.Menu.objects.prefetch_related('categories').all()
    serializer_class = RetrieveMenuSerializer


class RetrieveCategoryAPI(RetrieveModelMixin, GenericViewSet):
    queryset = models.Category.objects.prefetch_related('products').all()
    serializer_class = RetrieveCategorySerializer


class RetrieveProductAPI(RetrieveModelMixin, GenericViewSet):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
