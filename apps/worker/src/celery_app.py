from apps.api.src.core.config import settings

from celery import Celery

celery_app = Celery(f"{settings.app_vertical}_copilot")
celery_app.conf.broker_url = settings.redis_url
celery_app.conf.result_backend = settings.redis_url.replace("/0", "/1") if settings.redis_url.endswith("/0") else settings.redis_url
