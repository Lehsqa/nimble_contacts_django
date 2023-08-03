from rest_framework import views
from rest_framework.response import Response
from .utils import full_text_search


class ContactFullTextSearchView(views.APIView):
    def get(self, request, format=None):
        search_text = request.GET.get('search')
        results = full_text_search(search_text)
        return Response({'results': results})
