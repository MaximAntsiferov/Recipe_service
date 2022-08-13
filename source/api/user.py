from typing import List
from fastapi import APIRouter
from source.db import database, users
from source.models.user import User

router = APIRouter(prefix="/users")


@router.get("/", response_model=User)
async def get_user(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)


@router.get("/top10", response_model=List[User])
async def get_top10(limit: int = 10, skip: int = 0):
    query = users.select()
    return await database.fetch_all(query)
