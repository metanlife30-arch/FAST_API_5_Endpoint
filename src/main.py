from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from .repository import WalletRepository
from .models.wallet import Wallet 
from .schemas.wallet import WalletСhange, WalletResponce
from .services import WalletsService
from .dependencies import wallets_service
# Создание экземпляра FastAPI
app = FastAPI()

# Эндпоинт для создание кошешька
@app.post("/api/v1/wallets/create", status_code=201, responses={201: {"description":"Wallet Created"},500: {"description":"Internal server error"}}, response_model=WalletResponce, summary="Create a wallet", description="Сreates a wallet for the user",tags=["Wallets"])
async def wallet_add( wallets_service: Annotated[WalletsService, Depends(wallets_service)])->WalletResponce:
    # Поиск автора поста по ID
    post =await wallets_service.wallet_create()
    return post
    
# Эндпоинт для изменение баланса
@app.put("/api/v1/wallets/operation", response_model= WalletResponce, responses={200: {"description":"The wallet has been updated"},404: {"description":"Wallet not found"},500: {"description":"Internal server error"}}, summary="Changing the balance", description="Changes the amount of the user's wallet",tags=["Wallets"])
async def wallet_change(wallet:Annotated[WalletСhange,Query()],wallets_service: Annotated[WalletsService, Depends(wallets_service)])->WalletResponce:
    # Условие если было введенно DEPOSIT 
    result = await wallets_service.change_wallet(wallet)
    if result == "not found":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    elif result == "The withdrawal amount is more than what is on the balance":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The withdrawal amount is more than what is on the balance')
    return result
    


# Эндпоинт для удаление кошешька
@app.delete("/api/v1/wallets/delete", responses={200: {"description":"Wallet Deleted"},404: {"description":"Wallet not found"},500: {"description":"Internal server error"}}, summary="Delete a wallet",tags=["Wallets"])
async def delete_wallet(id_wallet: Annotated[int,Query(..., description="Deletes the user's wallet by id")],
                        wallets_service: Annotated[WalletsService, Depends(wallets_service)])->dict:
    # Поиск кошелька по ID
    delete = await wallets_service.wallet_delete(id_wallet)
    if delete == "not found":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    return {"message": "Wallet successfully deleted"} 

#Эндпоинт для получение всех кошельков
@app.get("/api/v1/wallets/list", response_model=list[WalletResponce], responses={200: {"description":"The list of wallets is ready"},404: {"description":"Wallets not found"},500: {"description":"Internal server error"}},summary="Get a list of all wallets", description="Retrieves all data for all user wallets",tags=["Wallets"])
async def get_all_wallets(wallets_service: Annotated[WalletsService, Depends(wallets_service)]):
    wallets = await wallets_service.list_wallets()
    return wallets

#Эндпоинт для получение определенного кошелька
@app.get("/api/v1/wallets/get/{id}", response_model=WalletResponce, responses={200: {"description":"Wallet found"},500: {"description":"Internal server error"}}, summary="Getting a balance", description="Retrieves data for a specific wallet",tags=["Wallets"])
async def wallet_get(id: Annotated[int,Path(..., title="id wallet", description="Get a wallet by ID")],
                     wallets_service: Annotated[WalletsService, Depends(wallets_service)])->WalletResponce:
    # Поиск кошелька по ID
    wallet = await wallets_service.get_wallet(id)
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    return wallet
    


