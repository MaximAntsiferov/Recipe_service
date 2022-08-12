import uvicorn
from fastapi import FastAPI

from source.api.recipes import router as recipes_router

from source.db import database, engine, metadata
from source.settings import settings

app = FastAPI()
app.include_router(recipes_router)


@app.on_event("startup")
async def startup_event():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    metadata.create_all(engine)
    uvicorn.run(
        "app:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )


