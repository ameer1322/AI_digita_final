from typing import Optional, List

from fastapi import APIRouter, HTTPException
from starlette import status
from model.product_update_quantity import ProductUpdateQuantity
from model.product_model import ProductModel

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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel):
    try:
        return await products_service.create_product(product.name, product.price,product.quantity)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.put("/{name}",status_code=status.HTTP_200_OK)
async def update_product(name:str, product: ProductModel):
    try:
        return await products_service.update_product(name,product.price,product.quantity)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.delete("/{name}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(name:str):
    try:
        await products_service.delete_product(name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/update_stock/{name}",status_code=status.HTTP_200_OK)
async def update_stock(name:str ,product_update_quantity :ProductUpdateQuantity):
    try:
        return await products_service.update_stock(name, product_update_quantity.quantity)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
