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
    # Метод слоя инфраструктуры для создание кошелька
    async def create_wallet(self) -> dict:
        async with async_session_local() as session:
            post = self.model(amount=0)
            session.add(post)
            await session.commit()
            return post
    
    # Метод слоя инфраструктуры для удаление кошелька
    async def delete_wallet(self,id):
        async with async_session_local() as session:
            delete = await session.get(self.model,id)
            if delete:
                await session.delete(delete)
                await session.commit()
            else:
                return "not found"
            
    # Метод слоя инфраструктуры для изменение баланса
    async def wallet_change(self,wallet:dict)->dict:
        async with async_session_local() as session:
            result = await session.get(self.model,wallet.id)
            result.amount =  wallet.amount 
            await session.commit()
            return result
        
    # Метод слоя инфраструктуры для получение определенного кошелька
    async def wallet_get(self,id:int)->dict:
        async with async_session_local() as session:
            # Поиск кошелька по ID
            wallet = await session.get(self.model, id)
            return wallet
        
    # Метод слоя инфраструктуры для получение всех кошельков
    async def find_all(self)->list[dict]:
        async with async_session_local() as session:
            query = select(self.model)
            result = await session.execute(query)
            wallets = result.scalars().all()
            return wallets
        
   