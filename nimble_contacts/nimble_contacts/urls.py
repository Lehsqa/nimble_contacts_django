from django.contrib import admin
from django.urls import path
from contacts.views import ContactFullTextSearchView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/contacts-search', ContactFullTextSearchView.as_view(), name='contacts_search')
]
