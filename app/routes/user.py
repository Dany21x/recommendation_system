from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.models.user_preference import UserPreference
from app.database import get_db

router = APIRouter()

# Create user
@router.post("/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Agregar preferencias del usuario
    for category_id in user.preferences:
        db_preference = UserPreference(id_user=db_user.id_user, id_category=category_id)
        db.add(db_preference)
    db.commit()

    return db_user

# get all users
@router.get("/", response_model=list[UserCreate])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# get user by ID
@router.get("/{user_id}", response_model=UserCreate)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# update user
@router.put("/{user_id}", response_model=UserUpdate)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id_user == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # update user data
    for key, value in user.dict(exclude={'preferences'}).items():
        setattr(db_user, key, value)
    db.commit()

    # update user preferneces
    db.query(UserPreference).filter(UserPreference.id_user == user_id).delete()  # delete old preferences
    for category_id in user.preferences:
        db_preference = UserPreference(id_user=user_id, id_category=category_id)
        db.add(db_preference)
    db.commit()

    return db_user

# Delete user
@router.put("/{user_id}/delete", response_model=UserUpdate)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id_user == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}

    return db_user


