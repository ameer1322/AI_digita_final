from pydantic import BaseModel


class ProductReduceInventoryModel(BaseModel):
    product_id:int
    amount:int