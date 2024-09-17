from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'recommendation_system'}

    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
