from datetime import datetime
from models.account import Account

class VaultService:

    def __init__(
        self,
        storage,           
        encryption,        
        search_service     
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
            site=site,
            username=username,
            encrypted_password=encrypted,
            category_id=category_id
        )

        return self.storage.save_account(account)

    def list_accounts(self) -> list[Account]:
        return self.storage.get_all_accounts()

    def search_accounts(self, keyword: str) -> list[Account]:
        return self.search_service.global_search(keyword)