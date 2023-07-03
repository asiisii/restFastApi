from models import Item
from db import Base, engine

print("Creating database connection")

# Create the database tables (if they don't exist)
Base.metadata.create_all(bind=engine)


