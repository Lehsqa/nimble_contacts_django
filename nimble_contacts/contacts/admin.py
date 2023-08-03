from django.contrib import admin
from contacts.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    list_filter = ('first_name',)
    search_fields = ('first_name', 'last_name')


admin.site.register(Contact, ContactAdmin)
