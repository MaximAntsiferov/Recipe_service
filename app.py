import uvicorn
from fastapi import FastAPI, Depends

from source.api.auth import router as auth_router
from source.api.user import router as user_router
from source.api.recipes import router as recipes_router, get_recipes

from source.db import database, engine, metadata
from source.settings import settings

tags_metadata = [
    {
        "name": "Auth",
        "description": "Регистрация, авторизация, профиль"
    },
    {
        "name": "Users",
        "description": "Действия и операции с пользователями"
    },
    {
        "name": "Recipes",
        "description": "Действия и операции с рецептами"
    }
]

app = FastAPI(
    title="Recipe Service",
    description="Here you can share your best cooking practice",
    version="1.0.0b",
    openapi_tags=tags_metadata
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(recipes_router)


@app.on_event("startup")
async def startup_event():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    metadata.create_all(engine)
    uvicorn.run(
        "app:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )


