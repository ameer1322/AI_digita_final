
from pydantic import BaseModel

class OrderRequest(BaseModel):
    product_name : str
    quantity: int