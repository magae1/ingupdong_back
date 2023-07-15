from django.apps import AppConfig


class IngupdongConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ingeupdong'

    def ready(self):
        from . import scheduler
        from . import signals
        from rank.signals import score_on_channel
        scheduler.start()
        signals.after_crawl_trending.connect(score_on_channel,
                                             dispatch_uid="scores_on_channels_after_crawling")
