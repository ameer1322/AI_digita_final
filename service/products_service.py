from typing import Optional, List

from repository import products_repository

async def get_products():
    return await products_repository.get_products()

async def create_product(name:str, price:float, quantity:int):
    check_product_exists = await products_repository.get_product_by_name(name)
    if not check_product_exists:
        return await products_repository.create_product(name, price, quantity)
    raise Exception (f"Product with name {name} already exists, use add_product instead")