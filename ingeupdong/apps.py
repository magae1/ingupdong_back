from django.apps import AppConfig


class IngupdongConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ingeupdong'

    def ready(self):
        from . import signals
        from rank.signals import score_on_channel_by_trends
        signals.after_crawl_trending.connect(score_on_channel_by_trends,
                                             dispatch_uid="scores_on_channels_after_crawling")
