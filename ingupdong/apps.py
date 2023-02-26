from django.apps import AppConfig


class IngupdongConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ingupdong'

    def ready(self):
        from ingupdong.schedule.schedulers import start
        start()
