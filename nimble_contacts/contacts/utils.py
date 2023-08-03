import requests
import csv
import os
from datetime import datetime

from django.db import connection
from django.core.cache import cache
from .models import Contact


def response_get():
    url = "https://api.nimble.com/api/v1/contacts?fields=first%20name,last%20name,email&record_type=person"
    headers = {'Authorization': 'Bearer NxkA2RlXS3NiR8SKwRdDmroA992jgu'}
    response = requests.get(url=url, headers=headers)

    return response


def create_idx():
    cursor = connection.cursor()
    cursor.execute("DROP INDEX IF EXISTS contact_search_idx")
    cursor.execute("CREATE INDEX contact_search_idx ON contacts_contact USING gin (to_tsvector('english', first_name), "
                   "to_tsvector('english', last_name), to_tsvector('english', email))")
    connection.close()


def full_text_search(search: str):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM contacts_contact WHERE first_name @@ to_tsquery('{search}') "
                   f"OR last_name @@ to_tsquery('{search}') OR email @@ to_tsquery('{search}')")

    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def manual_update():
    contacts_to_update = []
    emails_csv = set()

    with open(os.path.join(os.getcwd(), 'nimble_contacts.csv'), 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            contacts_to_update.append(Contact(first_name=row[0], last_name=row[1], email=row[2]))
            emails_csv.add(row[2])

    response = response_get()

    if response.status_code == 200:
        contacts_data = response.json()['resources']

        for contact_data in contacts_data:
            first_name = contact_data['fields'].get('first name')[0].get('value')
            last_name = contact_data['fields'].get('last name')[0].get('value')
            email = contact_data['fields'].get('email')
            if email is not None:
                email = email[0].get('value')
            else:
                email = f'{first_name}.{last_name}@noexist.com'

            if email in emails_csv:
                continue

            if first_name and last_name:
                contacts_to_update.append(Contact(first_name=first_name, last_name=last_name, email=email))

    Contact.objects.all().delete()
    Contact.objects.bulk_create(contacts_to_update, update_conflicts=True,
                                unique_fields=['email'],
                                update_fields=['first_name', 'last_name'])

    create_idx()

    cache.set('LAST_UPDATE', str(datetime.now()), 86500)
    return cache.get('LAST_UPDATE')
