# Eventify Project Documentation

## Project Overview

**Eventify** is a comprehensive web application designed to streamline the process of discovering, comparing, and purchasing tickets for upcoming events. The platform facilitates a smooth user experience by allowing users to:

  * **Discover** a wide array of upcoming events.
  * **Compare** different ticket types, prices, and availability.
  * **Purchase** tickets with minimal friction.

## Setup & Installation

### Prerequisite

To run Eventify, you must have Docker installed.

  * Please install the **latest version** of Docker by visiting the official website: [https://www.docker.com/get-started/](https://www.docker.com/get-started/)

### Deployment

The application uses Docker Compose for environment setup.

Execute the following command in your terminal from the project's root directory:

```bash
docker compose up --build
```

### Post-Installation Steps

After the containers are running, you must set up the database and create an administrative user.

Apply database migrations to set up the schema:

```bash
docker exec -it eventfy-backend python manage.py migrate
```

Create a superuser account for accessing the administrative interface:

```bash
docker exec -it eventfy-backend python manage.py createsuperuser
```

## Access

Once the application is running, you can access it in your web browser:

- **Eventify Web App:** http://localhost:8080  
- **Admin Panel:** http://localhost:8000/admin  

---

Admin Credentials are as follows:
- **Username:** admin  
- **Password:** 123