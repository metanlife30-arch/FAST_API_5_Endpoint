from .schemas.wallet import WalletСhange, WalletResponce
from .utils.repository import AbstractRepository


class WalletsService:
    def __init__(self, wallets_repo: AbstractRepository):
        self.wallets_repo: AbstractRepository = wallets_repo()

    # Метод сервиса для создание кошешька
    async def wallet_create(self)->WalletResponce:
        post = await self.wallets_repo.create_wallet()
        return post
    
    # Метод сервиса для изменение баланса 
    async def change_wallet(self, wallet:WalletСhange):
        result = await self.wallets_repo.wallet_get(wallet.id)
        #Вызов бизнес логики (переход к Доменному слою)
        counting = await self._check(wallet,result)
        # Условие если была ошибка то возвращать Эндпоинту(слою Презентация)
        if isinstance(counting, str):
            return counting
        result = await self.wallets_repo.wallet_change(counting)
        return result

    # Метод сервиса для удаление кошелька
    async def wallet_delete(self, id: int):
        delete = await self.wallets_repo.delete_wallet(id)
        return delete
    
    # Метод сервиса для получение всех кошельков
    async def list_wallets(self)->list[WalletResponce]:
        wallets_list = await self.wallets_repo.find_all()
        return wallets_list
    
    # Метод сервиса для получение определенного кошелька
    async def get_wallet(self, id: int):
        wallet = await self.wallets_repo.wallet_get(id)
        return wallet
    
    # Доменный слой
    async def _check(self,wallet,result):
        if result :
            if wallet.operation_type=="DEPOSIT":
                # Условие сумма кошелька равна 0
                if result.amount==0 :
                    result.amount =  wallet.amount 
                    return result
                # Добавляем сумму на кошелёк
                result.amount =  result.amount + wallet.amount  
                return result
                    
            # Условие если было введенно WITHDRAW 
            else:  
                if wallet.amount <= result.amount: 
                    result.amount =  result.amount - wallet.amount  
                    return result
                # Условие если сумма снятие больше чем сумма на балансе
                return "The withdrawal amount is more than what is on the balance"
            
        # Условие если не был найден кошелёк
        return "not found"

