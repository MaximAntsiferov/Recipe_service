from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class UserStatus(str, Enum):
    active = "Активен"
    blocked = "Заблокирован"


class User(BaseModel):
    id: Optional[int] = None
    username: str
    status: UserStatus = "Активен"
    created_at: date
    updated_at: date
    hashed_password: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str
