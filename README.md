# Project Documentation

## Overview

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

Admin credentials are as follows:
- **Username:** admin  
- **Password:** 123

## Email Receipt Configuration for Ticket Purchases

To enable email receipts for ticket purchases, a **Gmail** account is required. Configure it using the steps below:

1. Set the sender email address by adding your email to `EMAIL_HOST_USER`  
   _(search for this variable in the project)_.

2. Generate a Google App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Create an app password
   - Copy the generated password

3. Add the generated password to `EMAIL_HOST_PASSWORD`.

After completing these steps, clicking **Send Receipt** in the **Purchased Tickets** window will send the receipt from the specified email address.
