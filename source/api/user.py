from datetime import datetime
from typing import List, Optional
from fastapi import status, APIRouter, Depends, Response
from sqlalchemy import select, desc, text, and_
from sqlalchemy.sql.functions import count

from source.db import database, users, recipes
from source.models.user import User, UserStatus, BaseUser, UserUpdate
from source.services.auth import get_current_active_user

router = APIRouter(prefix="/users")


@router.get("/", response_model=List[User])
async def get_users(status: Optional[UserStatus] = None):
    users_query = users.select()
    if status:
        users_query.filter_by(status=status)
    user_list = await database.fetch_all(users_query)
    return user_list


@router.get("/{username}", response_model=User)
async def get_user(username: str):
    user_query = users.select().where(users.c.username == username)
    user = await database.fetch_one(user_query)
    return user


@router.get("/top10", response_model=List[User])
async def get_top10_users():
    authors_and_recipes = select([recipes.c.author, count(recipes.c.id)]).select_from(recipes).group_by(recipes.c.author).order_by(desc(text('2')))
    sbqr = authors_and_recipes.subquery()
    users_and_recipes = select([sbqr, users]).where(sbqr.c.author == users.c.id).filter(users.c.status == "Активен").limit(10)
    top10_users = await database.fetch_all(users_and_recipes)
    return top10_users


@router.put('/{user_id}', response_model=User)
async def update_user(user_id: int, user_data: UserUpdate, user: BaseUser = Depends(get_current_active_user)):
    now = datetime.utcnow()
    user_data.dict()['update_at'] = now
    query = users.update().where(and_(users.c.id == user.id, users.c.id == user_id)).values(**user_data.dict())
    await database.execute(query)
    get_updated_user = users.select().where(and_(users.c.id == user.id, users.c.id == user_id))
    updated_user = await database.fetch_one(get_updated_user)
    return updated_user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(user_id: int, user: BaseUser = Depends(get_current_active_user)):
    query = users.delete().where(and_(users.c.id == user_id, users.c.id == user.id))
    await database.execute(query)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


