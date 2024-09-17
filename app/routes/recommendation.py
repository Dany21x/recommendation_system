from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.recommendation import RecommendationResponse
from app.models.user_preference import UserPreference
from app.models.product import Product
from app.database import get_db

router = APIRouter()

@router.get("/users/{user_id}/recommendations", response_model=list[RecommendationResponse])
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    preferences = db.query(UserPreference).filter(UserPreference.id_user == user_id).all()
    if not preferences:
        raise HTTPException(status_code=404, detail="The user has no preferences set")

    category_ids = [preference.id_category for preference in preferences]
    recommended_products = db.query(Product).filter(Product.id_category.in_(category_ids)).all()

    if not recommended_products:
        raise HTTPException(status_code=404, detail="No products available for the user's favorite categories")

    return recommended_products
