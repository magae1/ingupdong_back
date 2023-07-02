from django.apps import AppConfig


class IngupdongConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ingeupdong'

    def ready(self):
        from . import scheduler
        scheduler.start()
