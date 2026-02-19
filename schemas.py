from fastapi import Body
from pydantic import BaseModel
from typing import  Annotated, Optional
from pydantic import BaseModel, Field

# Модель данных для изменения баланса кошелька
class Wallet_Сhange(BaseModel):
    id: int = Field(...,description="id wallet")
    operation_type : str = Field(default="DEPOSIT or WITHDRAW",description="The type of operation for adding or withdrawing cash") 
    amount:  int = Field(...,description="The amount to withdraw or add money to")

class Wallet_Responce(BaseModel):
    id: int = Field(...,description="id wallet") 
    amount:  int = Field(...,description="The amount on the balance sheet")





