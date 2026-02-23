from ..database import Base
from sqlalchemy import Column, Integer
# Модель кошелька
class Wallet(Base):
    __tablename__ = 'Wallet'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)



