from typing import Optional, List

from fastapi import APIRouter, HTTPException
from starlette import status
from model.product_create_model import ProductCreateModel

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

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreateModel):
    try:
        return await products_service.create_product(product.name, product.price,product.quantity)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))