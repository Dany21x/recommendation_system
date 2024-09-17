from fastapi import FastAPI
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.user_preference import UserPreference
from app.routes import user, product, recommendation
from app.database import Base, engine

# if not exists, Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include Routes
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(recommendation.router, prefix="/recommendations", tags=["recommendations"])

@app.get('/')
def index():
    return {'message': 'Welcome!'}