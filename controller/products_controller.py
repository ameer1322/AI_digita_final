from typing import Optional, List

from fastapi import APIRouter, HTTPException
from starlette import status

from service import products_service

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/",status_code=status.HTTP_200_OK)
async def get_products():
    try:
        return await products_service.get_products()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
