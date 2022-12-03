from django.http import JsonResponse
from django_tenants.utils import schema_context
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet


class SetSchemaView:
    set_schema = True


class AppModelViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
    SetSchemaView
):
    """ Базовий контролер, який створює/редагує/виводить список/видаляє з правильною схемою
    """
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        try:
            with schema_context(request.schema_name):
                return super().dispatch(request, *args, **kwargs)
        except AttributeError:
            return JsonResponse({"message": "Restaurant does not exist"})
