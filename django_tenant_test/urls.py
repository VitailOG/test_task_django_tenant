from django.urls import path, include

urlpatterns = [
    path('', include('info_restaurant.urls')),
]
