from fastapi import HTTPException
from typing import Optional, List
from starlette import status

from model.order_request import OrderRequest

from model.order_request import OrderRequest
from repository import favorites_repository, order_product_repository
from service import products_service

async def handle_favorites(user_id:int,product_name:str):
    product_id = await products_service.get_product_id_by_name(product_name)
    product_in_favorites = await get_user_favorites_by_product_id(product_id,user_id)
    if product_in_favorites:
        return await favorites_repository.remove_from_favorites(user_id,product_id)
    else:
        return await favorites_repository.add_to_favorites(user_id,product_id)

async def get_user_favorites_by_product_id(product_id:int, user_id:int):
    return await favorites_repository.get_user_favorites_by_product_id(product_id, user_id)

async def get_user_favorites(user_id:int):
    return await favorites_repository.get_user_favorites(user_id)