from datetime import datetime
from typing import List, Optional
from fastapi import status, APIRouter, Depends, Response
from sqlalchemy import and_

from source.db import recipes, database, users
from source.models.recipes import Recipe, RecipeKind, RecipeStatus, RecipeCreate, RecipeUpdate
from source.models.user import BaseUser
from source.services.auth import get_current_active_user

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.post("/create", response_model=Recipe, status_code=status.HTTP_201_CREATED, )
async def create_recipe(recipe_data: RecipeCreate, user: BaseUser = Depends(get_current_active_user)):
    """
    Добавление нового рецепта
    """
    now = datetime.utcnow()
    recipe = Recipe(
        created_at=now,
        updated_at=now,
        author=user.id,
        **recipe_data.dict(),
    )
    values = {**recipe.dict()}
    values.pop("id", None)
    query = recipes.insert().values(**values)
    recipe_id = await database.execute(query)
    get_created_recipe = recipes.select().where(recipes.c.id == recipe_id)
    created_recipe = await database.fetch_one(get_created_recipe)
    update_recipes_quantity = users.update().where(users.c.id == user.id).values(
        {"recipes_quantity": (user.recipes_quantity + 1)})
    await database.execute(update_recipes_quantity)
    return created_recipe


@router.get("/", response_model=List[Recipe])
async def get_recipes(kind: Optional[RecipeKind] = None, recipe_status: Optional[RecipeStatus] = None, user: BaseUser = Depends(get_current_active_user)):
    """
    Получение списка рецептов
    - **kind** - Фильтр по типу блюда
    - **recipe_status** - Фильтр по статусу (Активен/Заблокирован)
    """
    query = recipes.select()
    if kind:
        query = query.filter_by(kind=kind)
    if recipe_status:
        query = query.filter_by(recipe_status=recipe_status)
    recipes_list = await database.fetch_all(query)
    return recipes_list


@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int, user: BaseUser = Depends(get_current_active_user)):
    """
    Получение рецепта по ID
    - **recipe_id** - ID рецепта
    """
    query = recipes.select().where(recipes.c.id == recipe_id)
    return await database.fetch_one(query)


@router.put('/{recipe_id}', response_model=Recipe)
async def update_recipe(recipe_id: int, recipe_data: RecipeUpdate, user: BaseUser = Depends(get_current_active_user)):
    """
    Изменение характеристик рецепта
    - **recipe_id** - ID изменяемого рецепта
    """
    now = datetime.utcnow()
    recipe_data.dict()['update_at'] = now
    query = recipes.update().where(and_(recipes.c.id == recipe_id, recipes.c.author == user.id)).values(**recipe_data.dict())
    await database.execute(query)
    get_updated_recipe = recipes.select().where(recipes.c.id == recipe_id)
    updated_recipe = await database.fetch_one(get_updated_recipe)
    return updated_recipe


@router.delete('/{recipe_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(recipe_id: int, user: BaseUser = Depends(get_current_active_user)):
    """
    Удаление рецепта
    - **recipe_id** - ID удаляемого рецепта
    """
    query = recipes.delete().where(and_(recipes.c.id == recipe_id, recipes.c.author == user.id))
    await database.execute(query)
    update_recipes_quantity = users.update().where(users.c.id == user.id).values({"recipes_quantity": (user.recipes_quantity - 1)})
    await database.execute(update_recipes_quantity)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


