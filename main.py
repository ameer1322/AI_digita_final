from fastapi import FastAPI
from repository.database import database

from controller.auth_controller import router as auth_router
from controller.users_controller import router as user_router
from controller.products_controller import router as product_router
from controller.order_controller import router as order_router
from controller.order_product_controller import router as order_product_router
from controller.favorites_controller import router as favorites_router
from controller.chat_route import router as chat_router

app = FastAPI()

app.include_router(order_product_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(favorites_router)
app.include_router(chat_router)


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()