from django.apps import AppConfig
from .inits.cloudinary_init import cloudinary_init

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        cloudinary_init()