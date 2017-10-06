# Objective Tracker

## Prerequisites

First, make sure you meet the prerequisites before starting installation.

- Install Docker
- Clone the repository

## Installation

__Docker-Compose containers__

Then, build and start the Docker container for the site and database.

```bash
docker-compose build
docker-compose up
```

__Site configuration__

Before the site can function properly, a few steps need to be made manually :
- Run the migrations in order to create the database schema;
- Create the first super user in order to access to the admin site. This is useful to create objectives and manage users.

```bash
# Run migrations
docker-compose run web python manage.py migrate

# Create first super user
docker-compose run web python manage.py createsuperuser
```
