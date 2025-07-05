from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from sqlalchemy import select
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config.settings import settings
from app.deps.db import SessionDep
from .models import RefreshToken, BlacklistRefreshToken


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(data: dict, expires_delta: timedelta, scope: str):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({
        "exp": expire,
        "scope": scope,
        "iss": "coffee-shop-api",
        "aud": "coffee-shop-users",
    })
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt, expire

def create_access_token(data: dict):
    return create_token(data, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), scope="access_token")

def create_refresh_token(data: dict):
    return create_token(data, timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES), scope="refresh_token")

def verify_token(token: str, expected_scope: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            issuer="coffee-shop-api",
            audience="coffee-shop-users",
        )
        if payload.get("scope") != expected_scope:
            raise HTTPException(status_code=401, detail="Invalid scope")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def save_refresh_token(db: SessionDep, user_id: int, token: str, expires_at):
    refresh = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(refresh)
    await db.commit()
    return refresh

async def get_refresh_token(db: SessionDep, token: str, type: str):
    token_model = RefreshToken
    if type == 'blacklist':
        token_model = BlacklistRefreshToken
    result = await db.execute(
        select(token_model).where(token_model.token == token)
    )
    return result.scalar_one_or_none()


async def is_token_blacklisted(db: SessionDep, token: str) -> bool:
    result = await db.execute(
        select(BlacklistRefreshToken).where(BlacklistRefreshToken.token == token)
    )
    blacklisted = result.scalar_one_or_none()
    return blacklisted is not None

async def add_token_to_blacklist(db: SessionDep, user_id: int, token: str, expires_at: datetime):
    blacklisted = BlacklistRefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.add(blacklisted)
    await db.commit()
    
async def delete_refresh_token(db: SessionDep, token: str, type: str):
    refresh = await get_refresh_token(db, token, type)
    if refresh:
        await db.delete(refresh)
        await db.commit()


