from rest_framework import routers

from info_restaurant.api import endpoints

router = routers.SimpleRouter()


router.register('retrieve-menu', endpoints.RetrieveMenuAPI, basename='retrieve-menu')

router.register('retrieve-category', endpoints.RetrieveCategoryAPI, basename='retrieve-category')

router.register('retrieve-product', endpoints.RetrieveProductAPI, basename='retrieve-product')

urlpatterns = []

urlpatterns += router.urls
