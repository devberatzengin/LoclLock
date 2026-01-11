from core.entities.account import Account
from core.interfaces.storage_port import StoragePort
from core.interfaces.encryption_port import EncryptionPort
from core.interfaces.search_port import SearchPort
from datetime import datetime

class VaultService:

    def __init__(
        self,
        storage: StoragePort,
        encryption: EncryptionPort,
        search_service: SearchPort
    ):
        self.storage = storage
        self.encryption = encryption
        self.search_service = search_service

    def add_account(
        self,
        site: str,
        username: str,
        plain_password: str,
        category_id: int
    ) -> int:

        encrypted = self.encryption.encrypt(plain_password)

        account = Account(
            id=None,
            site=site,
            username=username,
            encrypted_password=encrypted,
            category_id=category_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        return self.storage.save_account(account)

    def list_accounts(self) -> list[Account]:
        return self.storage.get_all_accounts()

    def search_accounts(self, keyword: str) -> list[Account]:
        accounts = self.storage.get_all_accounts()
        return self.search_service.search(keyword, accounts)
