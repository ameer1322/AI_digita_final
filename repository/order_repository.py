from typing import Optional, List

import json

from sqlalchemy.util import await_only

from model.order_request import OrderRequest
from repository.database import database

async def get_orders():
    query="""
    SELECT * FROM orders
    """
    return await database.fetch_all(query)

async def get_order_id_by_user(user_id : int):
    query="""
    SELECT order_id FROM orders
    WHERE user_id = :user_id AND order_status = FALSE
    """
    values ={"user_id":user_id}
    result = await database.fetch_one(query,values)
    return result

async def check_order_exists(order_id:int):
    query="""
    SELECT order_id FROM orders
    WHERE order_id = :order_id
    """
    values = {"order_id":order_id}
    result = await database.fetch_one(query,values)
    return result

async def create_new_order(user_id:int, shipping_address:str):
    query = """
    INSERT INTO orders (user_id, order_shipping_address)
    VALUES(:user_id, :order_shipping_address)
    """
    values = {"user_id":user_id, "order_shipping_address":shipping_address}
    return await database.execute(query,values)

async def create_new_order_product(order:OrderRequest, order_id, product_id:int):
    query = """
    INSERT INTO order_product (order_id, product_id, quantity)
    VALUES(:order_id, :product_id, :quantity)
    """
    values = {"order_id":order_id,"product_id":product_id,"quantity":order.quantity}
    await database.execute(query,values)

async def check_order_product(product_id: int, order_id:int):
    query="""
    SELECT * FROM order_product
    WHERE order_id = :order_id and product_id = :product_id
    """
    values = {"order_id":order_id, "product_id":product_id}
    return await database.fetch_one(query,values)

async def add_product_to_order(order:OrderRequest,order_id:int, product_id):
    query="""
    UPDATE order_product
    SET quantity = quantity+:quantity
    WHERE order_id = :order_id and product_id = :product_id
    """
    values = {"quantity":order.quantity,"order_id":order_id,"product_id":product_id}
    await database.execute(query,values)

async def delete_order(order_id:int):
    query="""
    DELETE FROM orders
    WHERE order_id = :order_id
    """
    values = {"order_id":order_id}
    await database.execute(query,values)

async def get_user_unconfirmed_order(user_id):
    query = """
    SELECT name, quantity, price, order_product.product_id, orders.order_id, orders.order_shipping_address FROM orders
    JOIN order_product ON orders.order_id = order_product.order_id
    JOIN products ON order_product.product_id = products.product_id
    WHERE user_id = :user_id AND order_status = FALSE
    """
    values = {"user_id": user_id}
    result = await database.fetch_all(query,values)
    return result

async def get_user_confirmed_orders(user_id):
    query = """
    SELECT name, quantity, price, orders.order_id, order_date, orders.order_shipping_address FROM orders
    JOIN order_product ON orders.order_id = order_product.order_id
    JOIN products ON order_product.product_id = products.product_id
    WHERE user_id = :user_id AND order_status = TRUE
    """
    values = {"user_id": user_id}
    result = await database.fetch_all(query,values)
    return result


async def remove_from_order(order_id:int, product_id:int, amount:int):
    query = """
    UPDATE order_product
    SET quantity = quantity - :amount
    WHERE order_id = :order_id AND product_id = :product_id
    """
    values = {"order_id":order_id, "product_id":product_id, "amount": amount}
    return await database.execute(query,values)

async def remove_product_if_zero(product_id):
    query="""
    DELETE FROM order_product
    WHERE product_id = :product_id AND quantity = 0
    """
    values = {"product_id":product_id}
    await database.execute(query,values)

async def confirm_order(user_id :int):
    query = """
    UPDATE orders
    SET order_status = TRUE
    WHERE user_id = :user_id AND order_status = FALSE
    """
    values = {"user_id":user_id}
    return await database.execute(query,values)