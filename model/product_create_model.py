from pydantic import BaseModel

class ProductCreateModel(BaseModel):
    name: str
    price: float
    quantity: int