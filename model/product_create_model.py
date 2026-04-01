from pydantic import BaseSettings

class ProductCreateModel(BaseSettings):
    name : str
    price : float
    quantity : int
