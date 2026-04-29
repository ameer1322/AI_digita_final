from fastapi import HTTPException
from typing import Optional, List
from starlette import status

from model.order_request import OrderRequest

from model.order_request import OrderRequest
from repository import order_repository, order_product_repository
from service import products_service

async def get_order_products():
    return await order_product_repository.get_order_products()