"""
Module for the casestudy Django app.

https://docs.djangoproject.com/en/4.2/ref/applications/
"""
from .celery import app as celery_app

__all__ = ("celery_app",)

