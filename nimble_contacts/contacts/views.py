from rest_framework import views
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from .utils import full_text_search
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@method_decorator(name='get', decorator=swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'search', openapi.IN_QUERY,
            description=('Full text search data'),
            type=openapi.TYPE_STRING,
            enum=['Oleg', 'Ken', 'Noname'],
            required=True
        ),
    ]
))
class ContactFullTextSearchView(views.APIView):
    def get(self, request, format=None):
        search_text = request.GET.get('search')
        results = full_text_search(search_text)
        return Response({'results': results})
