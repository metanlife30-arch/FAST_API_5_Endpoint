from abc import ABC, abstractmethod

from sqlalchemy import  select

from ..database import async_session_local


class AbstractRepository(ABC):

    @abstractmethod
    async def create_wallet():
        ...

    @abstractmethod
    async def delete_wallet():
        ...
    
    @abstractmethod
    async def wallet_change():
        ...

    @abstractmethod
    async def find_all():
        ...

    @abstractmethod
    async def wallet_get():
        ...


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def create_wallet(self) -> dict:
        async with async_session_local() as session:
            post = self.model(amount=0)
            session.add(post)
            await session.commit()
            return post
        
    async def delete_wallet(self,id):
        async with async_session_local() as session:
            delete = await session.get(self.model,id)
            if delete:
                await session.delete(delete)
                await session.commit()
            else:
                return "not found"

    async def wallet_change(self,wallet:dict):
        async with async_session_local() as session:
            result = await session.get(self.model,wallet.id)
            if result:
                if wallet.operation_type=="DEPOSIT":
                    # Условие сумма кошелька равна 0
                    if result.amount==0 :
                        result.amount =  wallet.amount 
                        await session.commit()
                        return result
                    # Добавляем сумму на кошелёк
                    result.amount =  result.amount + wallet.amount  
                    await session.commit()
                    return result
                
                # Условие если было введенно WITHDRAW 
                else:  
                    if wallet.amount <= result.amount: 
                        result.amount =  result.amount - wallet.amount  
                        await session.commit()
                        return result
                    return "The withdrawal amount is more than what is on the balance"
            # Условие если не бьл найден кошелёк
            else: 
                return "not found"

    async def wallet_get(self,id):
        async with async_session_local() as session:
            # Поиск кошелька по ID
            wallet = await session.get(self.model, id)
            return wallet

    async def find_all(self)->list[dict]:
        async with async_session_local() as session:
            query = select(self.model)
            result = await session.execute(query)
            wallets = result.scalars().all()
            return wallets
        
   