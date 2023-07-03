from sqlalchemy import Column, Integer, String, Boolean, Text
from db import Base


# Define a SQLAlchemy model for the database entity
class Item(Base):
    __tablename__ = "items"  # Set the table name

    id = Column(Integer, primary_key=True, index=True)  # Define an integer primary key column
    name = Column(String(255), index=True, nullable=False, unique=True)  # Define a string column for the item name
    description = Column(Text)  # Define a string column for the item description, `Text` column type is designed to store long-form textual data, and it doesn't have a predefined maximum length
    price = Column(Integer, nullable=False, index=True) # using index=True, database engine will be able to look up for items with a price range like this `session.query(Item).filter(Item.price > desired_price).all()` a lot quicker than without the index=True option
    on_sale=Column(Boolean, default=False, index=True)

    # so we don't get "models.Item object at 0x0000001Fasdfasdf>" when we try to log the Item's instance
    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', description='{self.description}'), price='{self.price}'), on_sale='{self.on_sale}')>"  # String representation of the model object
