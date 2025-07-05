from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import SessionDep
from app.deps.auth import get_current_user, admin_required

from app.schemas.user import UserDetail, UserUpdate
from app.services.user_dao import UserDAO
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserDetail,
    summary="Get current user",
    description="Retrieve the currently authenticated user's details."
)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "/",
    summary="List all users (admin only)",
    description="Retrieve a list of all users. Accessible only to admin users."
)
async def list_users(
    db: SessionDep,
    admin: User = Depends(admin_required)
) -> list[UserDetail]:
    users = await UserDAO.get_all(db)
    return users

@router.get(
    "/{id}",
    summary="Get user by ID (admin only)",
    description="Retrieve a user's details by their ID. Accessible only to admin users."
)
async def get_user_by_id(
    id: int,
    db: SessionDep,
    admin: User = Depends(admin_required)
) -> UserDetail:
    user = await UserDAO.get_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch(
    "/{id}",
    response_model=UserDetail,
    summary="Partially update user",
    description="""Partially update a user's details. Users can update 
    their own information. Admins can update any user."""
)
async def update_user(
    id: int,
    data: UserUpdate,
    db: SessionDep,
    current_user: User = Depends(get_current_user)
):
    user = await UserDAO.get_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if current_user.id != user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_user = await UserDAO.update(db, user, data.model_dump(exclude_unset=True))
    return updated_user

@router.delete(
    "/{id}",
    status_code=204,
    summary="Delete user (admin only)",
    description="Delete a user by their ID. Accessible only to admin users."
)
async def delete_user(
    id: int,
    db: SessionDep,
    admin: User = Depends(admin_required)
):
    user = await UserDAO.get_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await UserDAO.delete(db, user)
    return None
