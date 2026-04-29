from fastapi import HTTPException
from typing import Optional, List
from starlette import status

from model.order_request import OrderRequest

from model.order_request import OrderRequest
from repository import order_repository
from service import products_service


async def get_orders():
    return await order_repository.get_orders()

async def get_order_by_user(user_id:int):
    return await order_repository.get_order_by_user(user_id)

async def check_order_exists(order_id:int):
    return await order_repository.check_order_exists(order_id)

async def add_product_to_order(order : OrderRequest, order_id : int, product_id):
    return await order_repository.add_product_to_order(order, order_id, product_id)

async def create_new_order(order:OrderRequest,user_id:int):
    return await order_repository.create_new_order(user_id)

async def create_order_product(order: OrderRequest, order_id: int, product_id:int):
    return await order_repository.create_new_order_product(order, order_id, product_id)


async def handle_order(order : OrderRequest, user_id):
    product_id = await products_service.get_product_id_by_name(order.product_name)
    order_id = await get_order_by_user(user_id)
    if order_id:
        check_order_product = await order_repository.check_order_product(product_id, order_id)
        if check_order_product:
            return await add_product_to_order(order, order_id, product_id)
        return await order_repository.create_new_order_product(order, order_id, product_id)
    order_id = await create_new_order(order,user_id)
    print(order_id, "check")
    return await order_repository.create_new_order_product(order, order_id, product_id)


async def delete_order(order_id:int):
    order_exists = await check_order_exists(order_id)
    if order_exists:
        await order_repository.delete_order(order_id)
