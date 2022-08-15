from datetime import datetime
from typing import List, Optional
from fastapi import status, APIRouter, Depends, Response
from sqlalchemy import select, desc, text, and_
from sqlalchemy.sql.functions import count

from source.db import database, users, recipes
from source.models.user import User, UserStatus, BaseUser, UserUpdate
from source.services.auth import get_current_active_user, get_password_hash

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
async def get_users(user_status: Optional[UserStatus] = None, user: BaseUser = Depends(get_current_active_user)):
    """
    Получение списка пользователей
    - **recipe_status** - Фильтр по статусу (Активен/Заблокирован)
    """
    users_query = users.select()
    if user_status:
        users_query.filter_by(user_status=user_status)
    user_list = await database.fetch_all(users_query)
    return user_list


@router.get("/top", response_model=List[User])
async def get_top_users(user: BaseUser = Depends(get_current_active_user)):
    """
    Получение 10 активных пользователей с самым большим количеством рецептов в порядке убывания
    """
    print("asfdasf")
    authors_and_recipes = select([recipes.c.author, count(recipes.c.id)]).select_from(recipes).group_by(recipes.c.author).order_by(desc(text('2')))
    sbqr = authors_and_recipes.subquery()
    print(authors_and_recipes)
    users_and_recipes = select([sbqr, users]).where(sbqr.c.author == users.c.id).filter(users.c.user_status == "Активен").limit(10)
    top10_users = await database.fetch_all(users_and_recipes)
    print(top10_users)
    return top10_users


@router.put('/{user_id}', response_model=User)
async def update_user(user_id: int, user_data: UserUpdate, user: BaseUser = Depends(get_current_active_user)):
    """
    Изменение характеристик пользователя
    - **user_id** - ID пользователя
    """
    print("asaff")
    now = datetime.utcnow()
    user_data.dict()['update_at'] = now
    query = users.update().where(and_(users.c.id == user.id, users.c.id == user_id)).values(**user_data.dict())
    print(query)
    await database.execute(query)
    get_updated_user = users.select().where(and_(users.c.id == user.id, users.c.id == user_id))
    print(get_updated_user)
    updated_user = await database.fetch_one(get_updated_user)
    return updated_user


@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: int, user: BaseUser = Depends(get_current_active_user)):
    """
    Получение пользователя по ID
    - **user_id** - ID пользователя
    """
    user_query = users.select().where(and_(users.c.id == user_id, users.c.id == user.id))
    user = await database.fetch_one(user_query)
    return user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, user: BaseUser = Depends(get_current_active_user)):
    """
    Удаление пользователя
    """
    query = users.delete().where(and_(users.c.id == user_id, users.c.id == user.id))
    await database.execute(query)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



