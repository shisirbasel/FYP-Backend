# Bookrade Django REST Project

## Overview
This Django Rest project is built for Bookrade, an online book trading platform. It uses Django 4.1.7 and integrates various packages for authentication, WebSocket communication, and REST API.

## Project Structure

bookrade/
├── bookrade/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
├── core/
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ └── ...
├── chat/
│ ├── consumers.py
│ ├── routing.py
│ └── ...
├── manage.py
└── README.md

## Django Settings
## Environment Setup for .env File
Create a `.env` file in the project root directory with the following content:

```env
DJANGO_SECRET_KEY= "Your django Secret Key"
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=''
DJANGO_ADMIN_URL='admin/'
DJANGO_DOMAIN_NAME = ''

# DATABASE CONFIGURATION
POSTGRES_USER="Your Database User"
POSTGRES_PASSWORD="Your Database Password"
POSTGRES_HOST="127.0.0.1"
POSTGRES_PORT="5432"
POSTGRES_DB="Your Database Name"

# MAIL SERVER CONFIGURATION
DJANGO_EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
DJANGO_EMAIL_HOST='Email Host'
DJANGO_EMAIL_PORT=587
DJANGO_EMAIL_HOST_USER="Your App Email"
DJANGO_EMAIL_HOST_PASSWORD="Your App Password"
DJANGO_EMAIL_USE_TLS=True
```

### Base Settings
- **SECRET_KEY**: Replace `"Your django Secret Key"` with a secret key.
- **DEBUG**: Set to `True` for development.
- **ALLOWED_HOSTS**: Add allowed hosts for deployment.

## Running the Project
1. Install dependencies: `pip install -r requirements.txt`
2. Apply migrations: `python manage.py migrate`
3. Run the server: `python manage.py runserver`
### Installed Apps
- `daphne`, `channels`, `rest_framework`, `corsheaders`, `rest_framework_simplejwt`, etc.



### Middleware
- Security, session, CORS, authentication, CSRF protection.

### Database
- PostgreSQL database configuration.

### Authentication
- Custom user model and JWT authentication.

### Email
- SMTP configuration for sending emails.

### Media and Static Files
- Media and static file configurations.

### ASGI and Channels
- ASGI and WebSocket communication setup.

## Database Setup
Create a PostgreSQL database named `Your Database Name` with the provided credentials from the `.env` file. Import `bookrade.dmp` to set up the initial schema and data.


## Additional Notes
- `bookrade.dmp`: Import this dump file to set up the initial database schema and data.


