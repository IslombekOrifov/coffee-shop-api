from celery import Celery
from celery.schedules import crontab
from app.config.settings import settings

from app.models.user import User, VerifyCode
from app.custom_jwt.models import RefreshToken, BlacklistRefreshToken

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.beat_schedule = {
    "delete-unverified-users-everyday": {
        "task": "app.tasks.check_user_task.delete_unverified_users",
        "schedule": crontab(minute="*"),
    },
}

from app.tasks import send_mail_tasks, check_user_task