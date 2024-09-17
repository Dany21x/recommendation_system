from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import Product
from app.database import get_db

router = APIRouter()

# Create product
@router.post("/", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Get all products
@router.get("/", response_model=list[ProductCreate], description="Retrieve a list of all products available in the database.")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# Get Product by ID
@router.get("/{product_id}", response_model=ProductCreate)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id_product == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product noT found!")
    return product

# Update product
@router.put("/{product_id}", response_model=ProductCreate)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id_product == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found!")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    return db_product

# Delete product
@router.put("/{product_id}/delete", response_model=ProductCreate)
def delete_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id_product == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found!")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    return db_product