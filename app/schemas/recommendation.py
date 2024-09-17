from pydantic import BaseModel

class RecommendationResponse(BaseModel):
    id_product: int
    name: str
    description: str
    price: float
    stock: int