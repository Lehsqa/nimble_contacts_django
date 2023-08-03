from django.contrib.admin.apps import AdminConfig


class ContactsAdminConfig(AdminConfig):
    default_site = 'admin.NimbleContactsAdminSite'
