from .schemas.wallet import WalletСhange, WalletResponce
from .utils.repository import AbstractRepository


class WalletsService:
    def __init__(self, wallets_repo: AbstractRepository):
        self.wallets_repo: AbstractRepository = wallets_repo()

    async def wallet_create(self):
        post = await self.wallets_repo.create_wallet()
        return post
    
    async def change_wallet(self, wallet:WalletСhange):
        result = await self.wallets_repo.wallet_change(wallet)
        return result
    

    async def wallet_delete(self, id: int):
        delete = await self.wallets_repo.delete_wallet(id)
        return delete
    
    async def list_wallets(self):
        wallets_list = await self.wallets_repo.find_all()
        return wallets_list

    async def get_wallet(self, id: int):
        wallet = await self.wallets_repo.wallet_get(id)
        return wallet