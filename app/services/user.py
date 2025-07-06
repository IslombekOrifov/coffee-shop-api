from datetime import UTC, datetime, timedelta
from random import randint

from fastapi import HTTPException
from sqlalchemy import select

from app.custom_jwt.services import pwd_context
from app.deps.db import SessionDep
from app.models.user import User
from app.schemas.auth import CreateUser
from app.schemas.user import UserDetail
from app.services.user_dao import UserDAO, VerifyCodeDAO
from app.tasks.send_mail_tasks import send_email_task


async def create_user(data: CreateUser, db:SessionDep) -> UserDetail:
    existing_user = await db.execute(
        select(User).where(User.email == data.email)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already in use. ")
    
    hashed_password = pwd_context.hash(data.password)
    
    new_user = await UserDAO.create(db, data, hashed_password)
    
    code = str(randint(100000, 999999))
    expires_at = datetime.now(UTC) + timedelta(minutes=2)
    await VerifyCodeDAO.create(db, code=code, user_id=new_user.id, expires_at=expires_at)

    send_email_task.delay(
        to_email=new_user.email,
        subject="Welcome!",
        body=f"Use this code to verify your account. Code: {code}"
    )
    return UserDetail.model_validate(new_user, from_attributes=True)