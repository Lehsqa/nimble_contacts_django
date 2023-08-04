from datetime import datetime, timedelta

from django.core.cache import cache
from celery import shared_task
from .utils import response_get, create_idx, parse_data
from .models import Contact


@shared_task
def update_contacts():
    response = response_get()

    if response.status_code == 200:
        contacts_data = response.json()['resources']
        contacts_to_update = []

        for contact_data in contacts_data:
            data = parse_data(contact_data)

            try:
                last_update = datetime.strptime(cache.get('LAST_UPDATE'), '%Y-%m-%d %H:%M:%S.%f')
            except:
                last_update = datetime.now() - timedelta(days=1)
            if data.get('created_date') < last_update or data.get('updated_date') < last_update:
                continue

            if data.get('first_name') and data.get('last_name'):
                contacts_to_update.append(Contact(first_name=data.get('first_name'),
                                                  last_name=data.get('last_name'),
                                                  email=data.get('email')))

        if not contacts_to_update:
            return 0

        Contact.objects.bulk_create(contacts_to_update,
                                    update_conflicts=True,
                                    unique_fields=['email'],
                                    update_fields=['first_name', 'last_name'])

        create_idx()

        cache.set('LAST_UPDATE', str(datetime.now()), 86500)
