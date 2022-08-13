from typing import List, Optional
from fastapi import APIRouter
from source.db import recipes, database
from source.models.recipes import Recipe, RecipeKind

router = APIRouter(prefix="/recipes")


@router.get("/", response_model=List[Recipe])
async def get_recipes(kind: Optional[RecipeKind] = None):
    query = recipes.select()
    if kind:
        query.filter_by(kind=kind)
    return await database.fetch_all(query)


@router.get("/as", response_model=Recipe)
async def get_recipe(name):
    query = recipes.select().where(recipes.c.name == name)
    return await database.fetch_one(query)