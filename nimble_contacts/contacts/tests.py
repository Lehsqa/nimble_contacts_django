import pytest
from rest_framework.test import APIClient
from contacts.models import Contact


client = APIClient()


@pytest.mark.django_db
def test_get_data():
    response = client.get('/api/v1/contacts-search?search=Oleg')
    assert response.status_code == 201
    contact = Contact.objects.first().value()
    assert contact != response
