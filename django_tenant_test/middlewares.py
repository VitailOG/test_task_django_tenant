from rest_framework.views import APIView


class SetSchemaInRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user = None

    def __call__(self, request):
        self.user = APIView().initialize_request(request).user
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        klass_view = hasattr(view_func, 'view_class') and view_func.view_class or view_func.cls

        if not getattr(klass_view, 'set_schema', False):
            return

        if restaurant := getattr(self.user, 'restaurant', False):
            setattr(request, 'schema_name', restaurant.schema_name)
