from pydantic import BaseSettings, BaseModel


class ProductUpdateQuantity(BaseModel):
    quantity:int