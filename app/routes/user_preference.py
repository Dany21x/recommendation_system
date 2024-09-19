from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.models.user_preference import UserPreference
from app.database import get_db

router = APIRouter()

# Create user
@router.post("/", response_model=UserPreference)
def create_user_preference(user_preference: UserPreference, db: Session = Depends(get_db)):
    db_preference = UserPreference(id_user=user_preference.id_user, id_category=user_preference.id_category)
    db.add(db_preference)
    db.commit()
    db.refresh(db_preference)

    return db_preference

'''
    # Agregar preferencias del usuario
    for category_id in user_preference.preferences:
        db_preference = UserPreference(id_user=db_user.id_user, id_category=category_id)
        db.add(db_preference)
    db.commit()
'''
