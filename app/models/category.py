from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
#from .user_preference import user_preferences
#from .product import Product
#from .user import User

from app.database import Base

class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = {'schema': 'recommendation_system'}

    id_category = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)