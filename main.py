from fastapi import FastAPI
from repository.database import database

from controller.users_controller import router as user_router
from controller.products_controller import router as product_router

app = FastAPI()

app.include_router(product_router)
app.include_router(user_router)


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()