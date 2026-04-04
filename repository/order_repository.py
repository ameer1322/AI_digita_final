from typing import Optional, List

import json

from sqlalchemy.util import await_only

from model.order_model import Order
from repository.database import database

async def get_orders():
    query="""
    SELECT * FROM orders
    """
    return await database.fetch_all(query)

async def get_order_by_user(user_id : int):
    query="""
    SELECT order_id FROM orders
    WHERE user_id = :user_id
    """
    values ={"user_id":user_id}
    result = await database.fetch_one(query,values)
    return result

async def create_new_order(order :Order):
    query = """
    INSERT INTO orders (user_id)
    VALUES(:user_id)
    """
    values = {"user_id":order.user_id}
    return await database.fetch_one(query,values)

async def create_new_order_item(order:Order, order_id):
    query = """
    INSERT INTO order_item (order_id, item_id, quantity)
    VALUES(:order_id, :item_id, :quantity)
    """
    values = {"order_id":order_id,"item_id":order.item_id,"quantity":order.quantity}

    return await database.fetch_one(query,values)

async def check_order_item(order:Order):
    query="""
    SELECT * FROM order_item
    WHERE user_id = :user_id and item_id = :item_id
    """
    values = {"user_id":order.user_id, "item_id":order.item_id}
    return await database.fetch_one(query,values)

async def add_item_to_order(order:Order,order_id:int):
    query="""
    UPDATE order_item
    SET quantity = quantity+:quantity
    WHERE order_id = :order_id and item_id = :item_id
    """
    values = {"quantity":order.quantity,"order_id":order_id,"item_id":order.item_id}
