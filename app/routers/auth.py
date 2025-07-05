from datetime import datetime, timezone, UTC
from fastapi import APIRouter, HTTPException, status

from app.custom_jwt.services import (
    create_access_token, verify_token,
    get_refresh_token, delete_refresh_token, is_token_blacklisted,
    add_token_to_blacklist
)

from app.deps.db import SessionDep
from app.common.enums import UserStatus
from app.services.user import create_user
from app.services.user_dao import UserDAO, VerifyCodeDAO
from app.services.auth import generate_tokens
from app.schemas.auth import CreateUser, VerifyCodeSchema, LoginSchema, TokenReponse
from app.schemas.user import UserDetail


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="""Register a new user with email, password, and 
    optional first and last name. Returns the created user."""
)
async def signup(data: CreateUser, db: SessionDep) -> UserDetail:
    new_user = await create_user(data, db)
    return new_user

@router.post(
    "/verify",
    status_code=status.HTTP_200_OK,
    summary="Verify user account",
    description="Verify a user's account using the verification code sent to their email."
)
async def verify_account(data: VerifyCodeSchema, db: SessionDep):
    code = await VerifyCodeDAO.get_code(db, data.code, data.email)
    if not code:
        raise HTTPException(status_code=400, detail="Invalid code")
    if code.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="Code expired")
    user = await UserDAO.get_by_id(db, code.user_id)
    user.status = UserStatus.VERIFIED
    await db.commit()
    return {"message": "Account verified successfully"}

@router.post(
    "/login",
    summary="User login",
    description="Authenticate user and return access and refresh tokens."
)
async def login(data: LoginSchema, db: SessionDep) -> TokenReponse:
    tokens = await generate_tokens(data, db)
    return tokens

@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Refresh the access token using a valid refresh token."
)
async def refresh(token: str, db: SessionDep):
    if await is_token_blacklisted(db, token):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    db_token = await get_refresh_token(db, token, type="whitelist")
    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if db_token.expires_at < datetime.now(timezone.utc):
        await delete_refresh_token(db, token, type="whitelist")
        raise HTTPException(status_code=401, detail="Refresh token expired")
    
    payload = verify_token(token, expected_scope="refresh_token")
    user_id = payload.get("sub")
    new_access_token, _ = create_access_token({"sub": user_id})
    return {"access_token": new_access_token}

@router.post(
    "/logout",
    summary="Logout user",
    description="Logout the user and revoke their refresh token by adding it to the blacklist."
)
async def logout(token: str, db: SessionDep):
    payload = verify_token(token, expected_scope="refresh_token")
    db_token = await get_refresh_token(db, token, type="whitelist")
    user_id = int(payload.get("sub"))
    await add_token_to_blacklist(db, user_id, token, db_token.expires_at)
    await delete_refresh_token(db, token, type="whitelist")
    return {"message": "Logged out successfully"}



