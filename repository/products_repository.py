from typing import Optional, List

import json
from repository.database import database

async def get_products():
    query = """
        SELECT * FROM products
        WHERE quantity > 0
    """
    return await database.fetch_all(query)

async def get_product_by_name(name:str):
    query = """
    SELECT * FROM products WHERE name = :name
        """
    values = {"name": name}
    return await database.fetch_one(query, values)

async def create_product(name:str, price:float, quantity:int):
    query = """
    INSERT INTO products (name, price, quantity)
    VALUES (:name, :price, :quantity)
    """
    values = {"name": name, "price": price, "quantity": quantity}
    await database.execute(query,values)

