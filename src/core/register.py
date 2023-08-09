from dependency_injector import containers, providers

from src.auth.containers import Container as AuthContainer
from src.core.containers import Container as DatabaseContainer
from src.users.containers import Container as UserContainer
from src.wallet.containers import Container as WalletContainer


class RegisterContainer(containers.DeclarativeContainer):
    users_container = providers.Container(UserContainer)
    auth_container = providers.Container(AuthContainer)
    db_container = providers.Container(DatabaseContainer)
    wallet_container = providers.Container(WalletContainer)