from sqlalchemy import Table, Column, Integer, String, ForeignKey
from app.database import Base

class UserPreference(Base):
    __tablename__ = 'user_preferences'
    __table_args__ = {'schema': 'recommendation_system'}


    id_category = Column(Integer, ForeignKey('recommendation_system.categories.id_category', ondelete='CASCADE'), primary_key=True)
    id_user = Column(Integer, ForeignKey('recommendation_system.users.id_user', ondelete='CASCADE'), primary_key=True)
    #id_user = Column(Integer, primary_key=True)
    #id_category = Column(Integer, primary_key=True)