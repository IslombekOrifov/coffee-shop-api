from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None
    

class VerifyCodeSchema(BaseModel):
    email: EmailStr
    code: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    
    
class TokenReponse(BaseModel):
    access_token: str
    refresh_token: str