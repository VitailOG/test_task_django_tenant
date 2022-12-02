from django.urls import path
from rest_framework import routers

from .api import endpoints


router = routers.SimpleRouter()

router.register('restaurant', endpoints.RestaurantAPI, basename='restaurant')

router.register('menu', endpoints.MenusAPI, basename='menu')

router.register('category', endpoints.CategoryAPI, basename='category')

router.register('product', endpoints.ProductAPI, basename='product')

urlpatterns = [
    path('create-restaurant/', endpoints.CreateRestaurantAPI.as_view()),
]

urlpatterns += router.urls
