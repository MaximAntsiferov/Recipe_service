from typing import List
from fastapi import APIRouter
from source.db import recipe, database
from source.models.recipes import Recipe


router = APIRouter(prefix="/recipes")


@router.get("/", response_model=List[Recipe])
async def get_recipes():
    query = recipe.select()
    return await database.fetch_all(query)

