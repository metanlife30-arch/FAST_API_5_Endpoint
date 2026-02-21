from enum import Enum
from pydantic import BaseModel
from pydantic import BaseModel, Field

# Класс который определяет допустимые значения для поля в запросе
class Gender(str, Enum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'

# Модель данных для изменения баланса кошелька
class WalletСhange(BaseModel):
    id: int = Field(...,description="id wallet")
    operation_type : Gender = Field(default=..., description="The type of operation for adding or withdrawing cash") 
    amount:  int = Field(...,description="The amount to withdraw or add money to")

# Модель данных для вывода ответа для эндпоинта по данным в кошельке
class WalletResponce(BaseModel):
    id: int = Field(description="id wallet") 
    amount:  int = Field(description="The amount on the balance sheet")





