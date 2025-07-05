from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.deps.db import SessionDep
from app.config.dao import BaseDAO
from app.models.user import User, VerifyCode
from app.schemas.auth import CreateUser
from app.common.enums import UserStatus, Role


class UserDAO(BaseDAO):
    model = User
    
    @classmethod
    async def create(cls, db: SessionDep, data: CreateUser, hashed_pass: str) -> User:
        new_user = User(
            email=data.email.lower().strip(),
            password=hashed_pass,
            first_name=data.first_name,
            last_name=data.last_name,
            status=UserStatus.UNVERIFIED,
            role=Role.USER,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    
    @classmethod
    async def update(cls, db: SessionDep, user: User, data: dict) -> User:
        for field, value in data.items():
            setattr(user, field, value)
        await db.commit()
        await db.refresh(user)
        return user
    
    @classmethod
    async def delete(cls, db: SessionDep, user: User):
        await db.delete(user)
        await db.commit()


class VerifyCodeDAO:
    
    @staticmethod
    async def create(db: SessionDep, code: str, user_id: int, expires_at):
        verify_code = VerifyCode(
            code=code,
            user_id=user_id,
            expires_at=expires_at
        )
        db.add(verify_code)
        await db.commit()

    @staticmethod
    async def get_code(db: SessionDep, code: str, user_email: str):
        result = await db.execute(
            select(VerifyCode)
            .join(VerifyCode.user)
            .options(joinedload(VerifyCode.user))
            .where(VerifyCode.code == code, User.email == user_email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def delete(db: SessionDep, code_id: int):
        code_obj = await db.get(VerifyCode, code_id)
        if code_obj:
            await db.delete(code_obj)
            await db.commit()
