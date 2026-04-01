from typing import Optional, List

from repository import products_repository

async def get_products():
    return await products_repository.get_products()
