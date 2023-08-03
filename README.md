# Getting started with Nimble Contacts API

## Running

1) ### `docker-compose up -d --build`
2) ### `docker-compose run web python nimble_contacts/manage.py migrate`
3) ### `docker-compose run web python nimble_contacts/manage.py update_database` - collecting all data from nimble DB and csv file, need to start for correct work of system
4) ### `docker-compose run web python nimble_contacts/manage.py createsuperuser`
5) ### `docker-compose up`

## Available Paths

### `http://localhost:8000/admin` - admin panel for searching DB`s

### `http://localhost:8000/api/v1/swagger` - online documentation (Swagger UI)

### `http://localhost:8000/api/v1/contacts-search?search={text}` - get request for getting contacts by full text search

### `http://localhost:5555` - Celery monitoring