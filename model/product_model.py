from pydantic import BaseSettings, BaseModel


class ProductModel(BaseModel):
    name : str
    price : float
    quantity : int
