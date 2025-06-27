from django.apps import AppConfig
import sys

class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    def ready(self):
        if 'runserver' in sys.argv:
            from tracker.scheduler import start_scheduler
            start_scheduler()

