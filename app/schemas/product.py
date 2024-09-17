'''
To avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the file models.py with the
SQLAlchemy models, and the file schemas.py with the Pydantic models.

These Pydantic models define more or less a "schema" (a valid data shape).

So this will help us avoiding confusion while using both.
'''

from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    id_category: int

class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    id_category: int
