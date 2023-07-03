from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id:int
    name:str
    description:str
    price:int
    on_sale:bool


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/greeting/{name}")
async def greet(name:str):
    return {"message": f"Hello {name}"}

@app.get('/greet')
async def greet_optional(name:Optional[str]="random user"):
    return {"message": f"Hello {name}"}
    
@app.put('/item/{item_id}')
async def update_item(item_id:int, item:Item):
    return {
        "item": item.name,
        "description": item.description,
        "price": item.price,
        "on_sale": False
    }
    
