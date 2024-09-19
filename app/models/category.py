from sqlalchemy import Column, Integer, String

from app.database import Base

class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = {'schema': 'recommendation_system'}

    id_category = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)