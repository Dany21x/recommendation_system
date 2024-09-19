'''
To avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the directory models
with the SQLAlchemy models, and the directory models with the Pydantic models.

These Pydantic models (schemas) define more or less a "schema" (a valid data shape).

So this will help us avoiding confusion while using both.
'''

from pydantic import BaseModel

class RecommendationResponse(BaseModel):
    id_product: int
    name: str
    description: str
    price: float
    stock: int
    id_category: int