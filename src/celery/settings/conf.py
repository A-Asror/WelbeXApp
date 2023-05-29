from src.conf.manager import settings

from .beat import get_beat_schedules

redbeat_lock_key = None
redbeat_redis_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_BROKER_URL
backend = settings.CELERY_RESULT_BACKEND
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True
task_ignore_result = False
task_track_started = True
include = ['src.celery.tasks']
beat_schedule = get_beat_schedules()
