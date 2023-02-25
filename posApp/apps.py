from django.apps import AppConfig
import os


class posAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posApp'

    def ready(self):
        from posApp import jobs
        if os.environ.get('RUN_MAIN', None) != 'true':
            jobs.start()