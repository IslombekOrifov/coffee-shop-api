from pydantic import BaseModel, EmailStr

from app.common.enums import UserStatus, Role


class UserDetail(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    status: UserStatus
    role: Role
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: EmailStr = None
    first_name: str | None = None
    last_name: str | None = None