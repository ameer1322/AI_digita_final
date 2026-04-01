from typing import Optional, List

import json
from repository.database import database

async def get_products():
    query = """
        SELECT * FROM products
    """
    return await database.fetch_all(query)

async def create_product(name:str, price:float, quantity:int):
    query = """
    INSERT INTO products (name, price, quantity)
    VALUES (:name, :price, :quantity)
    """
    values = {"name": name, "price": price, "quantity": quantity}
    await database.execute(query,values)

async def update_product(name:str, price:float, quantity:int):
    query ="""
    UPDATE products
    SET name = :name, price = :price, quantity = :quantity
    WHERE name = :name
    """
    values = {"name":name,"price":price,"quantity":quantity}
    result = await database.execute(query,values)
    return result

async def delete_product(name:str):
    query="""
    DELETE FROM products 
    WHERE name = :name
    """
    values = {"name":name}
    await database.execute(query,values)


async def get_product_by_name(name:str):
    query = """
    SELECT * FROM products WHERE name = :name
        """
    values = {"name": name}
    return await database.fetch_one(query, values)

async def get_product_quantity_by_name(name:str):
    query="""
        SELECT quantity FROM products
        WHERE name = :name
    """
    values = {"name":name}
    return await database.fetch_one(query,values)



async def update_stock(name:str, quantity:int):
    query = """
    UPDATE products
    SET quantity = quantity + :quantity 
    WHERE name = :name
    """
    values = {"name":name,"quantity":quantity}
    result = await database.execute(query,values)
    return result
