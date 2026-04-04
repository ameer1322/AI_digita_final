from typing import Optional, List

from fastapi import APIRouter, HTTPException
from starlette import status
from model.order_model import Order

from service import order_service

router = APIRouter(
    prefix="/order",
    tags=["order"]
)

@router.get("/",status_code=status.HTTP_200_OK)
async def get_orders():
    return await order_service.get_orders()

@router.put("/",status_code=status.HTTP_201_CREATED)
async def new_order(order : Order):
    return await order_service.new_order(order)


