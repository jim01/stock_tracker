import os
os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "casestudy.settings"


"""
Celery Scheduler config
"""

from celery import Celery

app = Celery('casestudy', broker='redis://redis')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
