from pydantic import BaseSettings

class ProductAddModel(BaseSettings):
    name:str
    quantity:int