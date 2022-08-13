from datetime import date
from enum import Enum
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
    id: int
    author: int
    created_at: date
    updated_at: date
    name: str
    kind: RecipeKind
    description: str
    cooking_steps: str
    photo: str
    likes: int
    status: RecipeStatus = "Активен"

    class Config:
        orm_mode = True

