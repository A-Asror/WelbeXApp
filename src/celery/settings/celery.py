from __future__ import absolute_import, unicode_literals

from celery import Celery

from src.conf.manager import settings

celery = Celery('celery', broker=settings.CELERY_BROKER_URL)

celery.config_from_object('src.celery.settings.conf')
