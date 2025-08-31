from django.apps import AppConfig


class TheaterCmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'theater_cms'
    
    def ready(self):
        """Import admin modules when the app is ready"""
        # This ensures all admin registrations are loaded
        from . import admin