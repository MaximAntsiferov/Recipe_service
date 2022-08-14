from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class RecipeKind(str, Enum):
    salad = "Салат"
    first_course = "Первое блюдо"
    second_course = "Второе блюдо"
    dessert = "Десерт"
    drink = "Напиток"
    bakery = "Выпечка"


class RecipeStatus(str, Enum):
    active = "Активен"
    blocked = "Заблокирован"


class Recipe(BaseModel):
    id: Optional[int] = None
    author: int
    created_at: date
    updated_at: date
    name: str
    kind: RecipeKind
    description: str
    cooking_steps: Optional[str] = None
    photo: str
    likes: int = 0
    recipe_status: RecipeStatus = "Активен"

    class Config:
        orm_mode = True


class RecipeCreate(BaseModel):
    name: str
    kind: RecipeKind
    description: str
    cooking_steps: str
    photo: str

    class Config:
        orm_mode = True


class RecipeUpdate(RecipeCreate):
    pass