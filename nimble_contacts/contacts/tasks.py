from datetime import datetime, timedelta

from django.core.cache import cache
from celery import shared_task
from .utils import response_get, create_idx
from .models import Contact


@shared_task
def update_contacts():
    response = response_get()

    if response.status_code == 200:
        contacts_data = response.json()['resources']
        contacts_to_update = []

        for contact_data in contacts_data:
            created_date = datetime.strptime(contact_data['created'][:10], '%Y-%m-%d')
            updated_date = datetime.strptime(contact_data['updated'][:10], '%Y-%m-%d')
            try:
                last_update = datetime.strptime(cache.get('LAST_UPDATE'), '%Y-%m-%d %H:%M:%S.%f')
            except:
                last_update = datetime.now() - timedelta(days=1)
            if created_date < last_update or updated_date < last_update:
                continue

            first_name = contact_data['fields'].get('first name')[0].get('value')
            last_name = contact_data['fields'].get('last name')[0].get('value')
            email = contact_data['fields'].get('email')
            if email is not None:
                email = email[0].get('value')

            if first_name and last_name:
                contacts_to_update.append(Contact(first_name=first_name, last_name=last_name, email=email))

        if not contacts_to_update:
            return 0

        Contact.objects.bulk_create(contacts_to_update,
                                    update_conflicts=True,
                                    unique_fields=['email'],
                                    update_fields=['first_name', 'last_name'])

        create_idx()

        cache.set('LAST_UPDATE', str(datetime.now()), 86500)
