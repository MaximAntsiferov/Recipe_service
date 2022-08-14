from typing import List
from fastapi import APIRouter
from sqlalchemy import select, desc, text
from sqlalchemy.sql.functions import count

from source.db import database, users, recipes
from source.models.user import User

router = APIRouter(prefix="/users")


@router.get("/", response_model=User)
async def get_user(username: str):
    user_query = users.select().where(users.c.username == username)
    user = await database.fetch_one(user_query)
    return user


@router.get("/top10", response_model=List[User])
async def get_top10():
    authors_and_recipes = select([recipes.c.author, count(recipes.c.id)]).select_from(recipes).group_by(recipes.c.author).order_by(desc(text('2')))
    sbqr = authors_and_recipes.subquery()
    users_and_recipes = select([sbqr, users]).where(sbqr.c.author == users.c.id).filter(users.c.status == "Активен").limit(10)
    top10_users = await database.fetch_all(users_and_recipes)
    return top10_users



