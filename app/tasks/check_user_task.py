from datetime import UTC, datetime, timedelta

from app.config.database import SessionLocal
from app.models.user import User, UserStatus

from .celery import celery_app


@celery_app.task(name="app.tasks.check_user_task.delete_unverified_users")
def delete_unverified_users():
    print("Deleting started")
    db = SessionLocal()
    try:
        cutoff_date = datetime.now(UTC) - timedelta(days=2)
        users_to_delete = db.query(User).filter(
            User.status == UserStatus.UNVERIFIED,
            User.created_at < cutoff_date
        ).all()
        deleted_count = len(users_to_delete)
        for user in users_to_delete:
            db.delete(user)
        db.commit()
        print(f"Deleted {deleted_count} unverified users")
    except Exception as e:
        db.rollback()
        print(f"Error deleting unverified users: {e}")
        raise
    finally:
        db.close()
