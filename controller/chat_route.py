from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from config import config
from service import products_service

router = APIRouter(prefix="/chat", tags=["chat"])
client = OpenAI()


class ChatRequest(BaseModel):
    message: str
    history: list[dict]


@router.post("/")
async def chat(request: ChatRequest):
    products = await products_service.get_products()

    product_list = ""
    for p in products:
        product_list += f"- {p['name']}: ${p['price']}, inventory: {p['inventory']}\n"

    system_prompt = f"""You are a helpful shopping assistant for our store. 
Here are the available products:
{product_list}
Answer questions about these products only."""

    messages = [{"role": "system", "content": system_prompt}] + request.history + [
        {"role": "user", "content": request.message}]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))