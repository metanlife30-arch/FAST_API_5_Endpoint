from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query, status
from sqlalchemy import select
from models import Wallet 
from database import  async_session_local
from schemas import Wallet_Сhange, Wallet_Responce


# Создание экземпляра FastAPI
app = FastAPI()

# Эндпоинт для создание кошешька
@app.post("/api/v1/wallets/create", status_code=201, responses={201: {"description":"Wallet Created"},500: {"description":"Internal server error"}}, response_model=Wallet_Responce, summary="Create a wallet", description="Сreates a wallet for the user",tags=["Wallets"])
async def wallet_add()->Wallet_Responce:
    # Поиск автора поста по ID
    async with async_session_local() as session:
        post = Wallet(amount=0)
        session.add(post)
        await session.commit()
        return post
    
# Эндпоинт для изменение баланса
@app.put("/api/v1/wallets/operation", response_model= Wallet_Responce, responses={200: {"description":"The wallet has been updated"},404: {"description":"Wallet not found"},500: {"description":"Internal server error"}}, summary="Changing the balance", description="Changes the amount of the user's wallet",tags=["Wallets"])
async def wallet_change(wallet:Wallet_Сhange)->Wallet_Responce:
    async with async_session_local() as session:
        # Условие если пользователь ввёл "DEPOSIT" or "WITHDRAW" идём дальше
        if wallet.operation_type=="DEPOSIT" or "WITHDRAW":  
            # Условие если не был ввёд id кошелька

            if wallet.operation_type=="DEPOSIT":
                result = await session.get(Wallet, wallet.id)
                # Условие если не бьл найден кошелёк
                if not result:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
                # Условие сумма кошелька равна 0    
                elif result.amount==0 :
                    result.amount =  wallet.amount 
                    await session.commit()
                    return result
                # Добавляем сумму на кошелёк
                result.amount =  result.amount + wallet.amount  
                await session.commit()
                return result
            
            else:
                # Условие если было введенно WITHDRAW
                result = await session.get(Wallet, wallet.id)
                # Условие если не бьл найден кошелёк 
                if not result:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')    

                elif wallet.amount <= result.amount: 
                    result.amount =  result.amount - wallet.amount  
                    await session.commit()
                    return result
                
                # Сумма снятия больше сумме на балансе
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The withdrawal amount is more than what is on the balance')
        # Ошибка на введённый не правильный тип операции                            
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid operation type')


# Эндпоинт для удаление кошешька
@app.delete("/api/v1/wallets/delete", responses={200: {"description":"Wallet Deleted"},404: {"description":"Wallet not found"},500: {"description":"Internal server error"}}, summary="Delete a wallet",tags=["Wallets"])
async def add_item(id_wallet: Annotated[int,Query(..., description="Deletes the user's wallet by id")])->dict:
    # Поиск кошелька по ID
    async with async_session_local() as session:
        delete = await session.get(Wallet,id_wallet)
        await session.delete(delete)
        await session.commit()
        return {"message": "Wallet successfully deleted"} 

#Эндпоинт для получение всех кошельков
@app.get("/api/v1/wallets/list", response_model=list[Wallet_Responce], responses={200: {"description":"The list of wallets is ready"},404: {"description":"Wallets not found"},500: {"description":"Internal server error"}},summary="Get a list of all wallets", description="Retrieves all data for all user wallets",tags=["Wallets"])
async def get_all_wallets():
    async with async_session_local() as session:
        query = select(Wallet)
        result = await session.execute(query)
        wallets = result.scalars().all()
        return wallets

#Эндпоинт для получение определенного кошелька
@app.get("/api/v1/wallets/get/{id}", response_model=Wallet_Responce, responses={200: {"description":"Wallet found"},500: {"description":"Internal server error"}}, summary="Getting a balance", description="Retrieves data for a specific wallet",tags=["Wallets"])
async def wallet_get(id: Annotated[int,Path(..., title="id wallet", description="Get a wallet by ID")])->Wallet_Responce:
    async with async_session_local() as session:
        # Поиск кошелька по ID
        wallet = await session.get(Wallet, id)
        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
        return wallet
    


