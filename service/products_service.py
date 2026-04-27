from fastapi import HTTPException
from typing import Optional, List
from starlette import status

from repository import products_repository

async def get_products():
    return await products_repository.get_products()

async def create_product(name:str, price:float, quantity:int):
    check_product_exists = await products_repository.get_product_by_name(name)
    if not check_product_exists:
        return await products_repository.create_product(name, price, quantity)
    raise ValueError(f"Product with name {name} already exists, use add_product instead")

async def update_product(name:str,price:float,quantity:int):
    check_product_exists = await products_repository.get_product_by_name(name)
    if not check_product_exists:
        raise ValueError(f"Product with name {name} doesn't exist")
    try:
        await products_repository.update_product(name,price,quantity)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = str(e))

async def delete_product(name:str):
    check_product_exists = await products_repository.get_product_by_name(name)
    if not check_product_exists:
        raise ValueError(f"Product with name {name} doesn't exist")
    try:
        await products_repository.delete_product(name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = str(e))


async def update_stock(name:str, quantity:int):
    check_product_exists = await products_repository.get_product_by_name(name)
    if not check_product_exists:
        raise ValueError(f"Product with name {name} doesn't exist")
    check_amount = await products_repository.get_product_quantity_by_name(name)
    if quantity >= 0:
        return await products_repository.update_stock(name,quantity)
    if check_amount[0] < -quantity:
        raise ValueError("Not enough products left in stock")
    return await products_repository.update_stock(name,quantity)

async def get_products_by_name(products:str):
    return await products_repository.get_products_by_name(products)