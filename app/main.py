from fastapi import FastAPI
from app.routes import user, product, recommendation, auth
from app.database import Base, engine
import uvicorn
from app.services.populate_data import populate_data

# if not exists, Create tables
Base.metadata.create_all(bind=engine)

populate_data()

app = FastAPI()

# Include Routes
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(recommendation.router, prefix="/recommendations", tags=["recommendations"])
app.include_router(auth.router, prefix="/token", tags=["token"])

@app.get('/')
def index():
    return {'message': 'Welcome to recommendation system!'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)