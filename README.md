# Django Rest Framework

## Instalacion

```bash
pip install djangorestframework
pip install cloudinary
pip install python-dotenv
pip install psycopg2-binary
```

## Configuracion

```python
# settings.py
from cloudinary import config
from os import environ
from dotenv import load_dotenv
```

```python
INSTALLED_APPS = [
    ...
    'ecommerce',
    'rest_framework',
    'cloudinary',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('DB_NAME'),
        'USER': environ.get('DB_USER'),
        'PASSWORD': environ.get('DB_PASSWORD'),
        'HOST': environ.get('DB_HOST'),
        'PORT': environ.get('DB_PORT'),
    }
}
```

```python
config(
    cloud_name = environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = environ.get('CLOUDINARY_API_KEY'),
    api_secret = environ.get('CLOUDINARY_API_SECRET'),
)
```

# Ejecutar migraciones

```bash
python manage.py makemigrations ecommerce
python manage.py migrate
```
