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
async def handle_order(order : Order):
    return await order_service.handle_order(order)

@router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id : int):
    return await order_service.delete_order(order_id)
