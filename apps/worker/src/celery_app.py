from celery import Celery

celery_app = Celery("sports_bet_copilot")
celery_app.conf.broker_url = "redis://redis:6379/0"
celery_app.conf.result_backend = "redis://redis:6379/1"
