from sqlalchemy import Column, ForeignKey, Integer, Float, DATE, func
from sqlalchemy.orm import relationship

from app.database import Base

class Purchase(Base):
    __tablename__ = 'purchases'
    __table_args__ = {'schema': 'recommendation_system'}

    id_purchase = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    id_user = Column(Integer, ForeignKey('recommendation_system.users.id_user', ondelete='CASCADE'))
    id_product = Column(Integer, ForeignKey('recommendation_system.products.id_product', ondelete='CASCADE'))
    purchase_date = Column(DATE, server_default=func.now())

    user = relationship('User')
    product = relationship('Product')