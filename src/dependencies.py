from .repository import WalletRepository
from .services import WalletsService



def wallets_service():
    return WalletsService(WalletRepository)