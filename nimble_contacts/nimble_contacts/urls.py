from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from contacts.views import ContactFullTextSearchView


schema_view = get_schema_view(
   openapi.Info(
      title="Nimble Contacts API",
      default_version='v1',
      description="Documentation of Nimble Contacts API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',
         include([
             path('contacts-search', ContactFullTextSearchView.as_view(), name='contacts-search'),
             path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
         ])
         ),
]
