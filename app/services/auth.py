from fastapi import HTTPException, status
from sqlalchemy import select

from app.custom_jwt.services import (
    pwd_context, create_access_token, 
    create_refresh_token, save_refresh_token
)

from app.deps.db import SessionDep
from app.services.user_dao import UserDAO
from app.common.enums import UserStatus
from app.schemas.auth import CreateUser, LoginSchema, TokenReponse


async def generate_tokens(data: LoginSchema, db: SessionDep) -> TokenReponse:
    user = await UserDAO.get_one_by_filters(db, email=data.email)
    
    if not user or not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    elif user.status == UserStatus.UNVERIFIED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is not verified. Please verify your email to proceed."
        )
    access_token, _ = create_access_token({"sub": str(user.id), "role": user.role})
    refresh_token, expire = create_refresh_token({"sub": str(user.id)})
    await save_refresh_token(db, user.id, refresh_token, expire)
    return TokenReponse(access_token=access_token, refresh_token=refresh_token)

