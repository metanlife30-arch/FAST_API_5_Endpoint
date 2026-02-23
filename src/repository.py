from .models.wallet import Wallet
from .utils.repository import SQLAlchemyRepository


class WalletRepository(SQLAlchemyRepository):
    model = Wallet