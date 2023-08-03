from django.contrib import admin


class NimbleContactsAdminSite(admin.AdminSite):
    title_header = 'Nimble Contacts Admin'
    site_header = 'Nimble Contacts administration'
    index_title = 'Nimble Contacts site admin'
