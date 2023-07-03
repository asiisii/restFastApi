from typing import List, Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from db import SessionLocal
import models

app = FastAPI()
db = SessionLocal()  # Create a database session

# Pydantic 
class Item(BaseModel):
    id:int
    name:str
    description:str
    price:int
    on_sale:bool
    
    class Config: 
        orm_mode=True # By setting this, Pydantic will generate an ORM model for the Item


@app.get('/items', response_model=List[Item], status_code=200)
async def get_all_items():
    items=db.query(models.Item).all()
    if items is None:
        raise HTTPException(status_code=404, detail="Item not found")  # If items are not found, raise an HTTP exception
    return items  # Return all items
        

@app.get('/items/{item_id}', response_model=Item, status_code=status.HTTP_200_OK)
async def get_an_item(item_id:int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()  # Query the database for an item with the given ID
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")  # If item is not found, raise an HTTP exception
    return item  # Return the item

@app.post('/items', response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_an_item(item:Item):
    db_item = db.query(models.Item).filter(models.Item.name == item.name).first() 
    
    if db_item is not None:
        raise HTTPException(status_code=404, detail="Item already exists")
    # new_item = models.Item(
    #     id=item.id,
    #     name=item.name,
    #     description=item.description,
    #     price=item.price,
    #     on_sale=item.on_sale
    # ) 
    # below is better way of writing it out
    new_item = models.Item(**item.dict())
    db.add(new_item)  # Add the new item to the session
    db.commit()  # Commit the session to save the changes to the database
    db.refresh(new_item)  # Refresh the item to get any database-generated values
    
    return new_item     # Return the newly created item, pydantic will automatically seralize our new_item object and give us back a json data

@app.put('/items/{item_id}', response_model=Item, status_code=status.HTTP_200_OK)
async def update_an_item(item_id:int, item:Item):
    item_to_update = db.query(models.Item).filter(models.Item.id == item_id).first()
    
    if not item_to_update:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for field, value in item.dict().items():
        setattr(item_to_update, field, value)
        
    db.commit()
    db.refresh(item_to_update)
    return item_to_update   

@app.delete('/items/{item_id}', status_code=status.HTTP_200_OK)
async def delete_an_item(item_id: int):
    item_to_delete = db.query(models.Item).filter(models.Item.id == item_id).first()
    
    if not item_to_delete:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item_to_delete)
    db.commit()
    return {"message": "Item successfully deleted"}
