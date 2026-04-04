from fastapi import HTTPException
from typing import Optional, List
from starlette import status

from model.order_model import Order
from repository import order_repository

async def get_orders():
    return await order_repository.get_orders()

async def get_order_by_user(user_id:int):
    return await order_repository.get_order_by_user(user_id)

async def add_item_to_order(order : Order, order_id : int):
    return await order_repository.add_item_to_order(order)

async def create_new_order(order:Order):
    return await order_repository.create_new_order(order)

async def create_order_item(order: Order, order_id: int):
    return await order_repository.create_new_order_item(order, order_id)


async def new_order(order : Order):
    order_id = await get_order_by_user(order.user_id)
    if order_id:
        check_order_item = await order_repository.check_order_item(order)
        if check_order_item:
            return add_item_to_order(order, order_id)
        return await order_repository.create_new_order_item(order, order_id)
    order_id = await create_new_order(order)
    return await order_repository.create_new_order_item(order, order_id)


