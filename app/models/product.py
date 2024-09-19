from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import relationship

from app.database import Base

class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'recommendation_system'}

    id_product = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    price = Column(Float)
    stock = Column(Integer)
    id_category = Column(Integer, ForeignKey('recommendation_system.categories.id_category', ondelete='CASCADE'))
    
    category = relationship('Category')