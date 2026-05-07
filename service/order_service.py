from fastapi import HTTPException
from typing import Optional, List

from numpy.ma.core import anomalies
from starlette import status

from model.order_request import OrderRequest

from model.order_request import OrderRequest
from repository import order_repository
from service import products_service, users_service


async def get_orders():
    return await order_repository.get_orders()

async def get_order_id_by_user(user_id:int):
    result = await order_repository.get_order_id_by_user(user_id)
    if result is None:
        return result
    return result[0]

async def check_order_exists(order_id:int):
    return await order_repository.check_order_exists(order_id)

async def add_product_to_order(order : OrderRequest, order_id : int, product_id):
    return await order_repository.add_product_to_order(order, order_id, product_id)

async def create_new_order(user_id:int, shipping_address: str):
    return await order_repository.create_new_order(user_id, shipping_address)

async def create_order_product(order: OrderRequest, order_id: int, product_id:int):
    return await order_repository.create_new_order_product(order, order_id, product_id)


async def handle_order(order : OrderRequest, user_id):
    product_id = await products_service.get_product_id_by_name(order.product_name)
    product_inventory = await products_service.get_inventory_by_id(product_id)
    order_id = await get_order_id_by_user(user_id)
    if order_id:
        check_order_product = await order_repository.check_order_product(product_id, order_id)
        if check_order_product:
            amount_in_user_order = check_order_product[2]
            if amount_in_user_order + order.quantity > product_inventory:
                raise ValueError("Order is bigger than inventory!")
            return await add_product_to_order(order, order_id, product_id)
        return await order_repository.create_new_order_product(order, order_id, product_id)
    shipping_address = await users_service.get_user_address(user_id)
    print(shipping_address[0])
    order_id = await create_new_order(user_id, shipping_address)
    return await order_repository.create_new_order_product(order, order_id, product_id)


async def delete_order(order_id:int):
    order_exists = await check_order_exists(order_id)
    if order_exists:
        await order_repository.delete_order(order_id)

async def get_user_unconfirmed_order(user_id):
    return await order_repository.get_user_unconfirmed_order(user_id)

async def get_user_confirmed_orders(user_id):
    return await order_repository.get_user_confirmed_orders(user_id)

async def remove_from_order(product_name:str,amount:int,user_id):
    order_id = await get_order_id_by_user(user_id)
    product_id = await products_service.get_product_id_by_name(product_name)
    result = await order_repository.remove_from_order(order_id,product_id,amount)
    await order_repository.remove_product_if_zero(product_id)
    order = await get_user_unconfirmed_order(user_id)
    if not order:
        await delete_order(order_id)
    return result

async def confirm_order(user_id:int):
    products_in_order = await get_user_unconfirmed_order(user_id)
    for product in products_in_order:
        product_id = product[3]
        product_order_amount = product[1]
        product_inventory = await products_service.get_inventory_by_id(product_id)
        if product_order_amount > product_inventory:
            raise ValueError("Not enough products in inventory!")
        await products_service.reduce_inventory(product_id, product_order_amount)
    return await order_repository.confirm_order(user_id)