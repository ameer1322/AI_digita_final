from pydantic import BaseModel

class RemoveFromOrderRequest(BaseModel):
    product_name:str
    amount:int