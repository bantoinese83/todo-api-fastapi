from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
