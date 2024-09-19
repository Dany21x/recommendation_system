from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.recommendation import RecommendationResponse
from app.models.user_preference import UserPreference
from app.models.user import User
from app.models.product import Product
from app.models.purchase import Purchase
from app.database import get_db
from app.services.analysis import segment_customer, generate_recommendations, transform_to_df
from app.auth import get_current_user

router = APIRouter()

@router.get("/{user_id}/favorites", response_model=list[RecommendationResponse])
def get_recommendations(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    preferences = db.query(UserPreference).filter(UserPreference.id_user == user_id).all()
    if not preferences:
        raise HTTPException(status_code=404, detail="The user has no preferences set")

    category_ids = [preference.id_category for preference in preferences]
    recommended_products = db.query(Product).filter(Product.id_category.in_(category_ids)).all()

    if not recommended_products:
        raise HTTPException(status_code=404, detail="No products available for the user's favorite categories")

    return recommended_products

@router.get("/{user_id}/similarity", response_model=list[RecommendationResponse])
def get_similarity_recommendations(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    purchases_query = db.query(Purchase, Product).join(Product, Purchase.id_product == Product.id_product).all()
    purchases = transform_to_df(purchases_query)
    cohort = segment_customer(purchases)
    user_segment = cohort[cohort.id_user == user_id].customer_segment.iloc[0]
    filtered_data = cohort[cohort['customer_segment'] == user_segment]
    segment = list(set(filtered_data['id_user']))
    df_segment = purchases[purchases['id_user'].isin(segment)]
    product_ids = generate_recommendations(user_id, df_segment, num_recommendations=5)

    product_recommendation = db.query(Product).filter(Product.id_product.in_(product_ids)).all()

    return list(product_recommendation)


@router.get("/{user_id}/historic", response_model=list[RecommendationResponse])
def get_recommendations(
    user_id: int,
    price_min: Optional[float] = Query(None, description="Minimum price filter"),
    price_max: Optional[float] = Query(None, description="Maximum price filter"),
    category_ids: Optional[list[int]] = Query(None, description="List of category IDs to filter by"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get historic purchases and preferences
    purchases = db.query(Purchase).filter(Purchase.id_user == user_id).all()
    purchased_product_ids = [purchase.id_product for purchase in purchases]

    preferences = db.query(UserPreference).filter(UserPreference.id_user == user_id).all()
    preferred_categories = [pref.id_category for pref in preferences]

    # Search for available products
    query = db.query(Product).filter(Product.stock > 0)

    if category_ids:
        query = query.filter(Product.id_category.in_(category_ids))
    else:
        query = query.filter(Product.id_category.in_(preferred_categories))

    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)

    recommended_products_by_category = query.all()

    # Exclude products already purchased
    recommended_products_by_category = [product for product in recommended_products_by_category
                                        if product.id_product not in purchased_product_ids]

    # Search purchased products
    similar_products = db.query(Product).filter(
        Product.id_product.in_(purchased_product_ids),
        Product.stock > 0
    ).all()

    recommended_products = recommended_products_by_category + similar_products

    # Drop duplicates
    recommended_products = list({product.id_product: product for product in recommended_products}.values())

    return recommended_products
