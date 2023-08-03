from rest_framework import viewsets, views
from rest_framework.response import Response
from .models import Contact
from .serializers import ContactSerializer
from .utils import full_text_search


class ContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactFullTextSearchView(views.APIView):
    def get(self, request, format=None):
        search_text = request.GET.get('search')
        results = full_text_search(search_text)
        return Response({'results': results})
