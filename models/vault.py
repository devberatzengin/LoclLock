"""
    Vault = koleksiyon mantigi.
   
     Yapar:
        tum account’lari tutar
        kategori bazli gruplar
        cache mantigi
        Bu sinif sayesinde controller SQL’i gormez.
    """

from typing import List
from models.account import Account


class Vault:
    def __init__(self, accounts: List[Account] | None = None):
        self._accounts: List[Account] = accounts or []

    # Basic operations
    def add_account(self, account: Account):
        self._check_duplicate(account)
        self._accounts.append(account)

    def remove_account(self, account_id: int):
        self._accounts = [
            acc for acc in self._accounts if acc.id != account_id
        ]

    def get_all_accounts(self) -> List[Account]:
        return list(self._accounts)

    # Find / Filter
    def find_by_category(self, category_id: int) -> List[Account]:
        return [
            acc for acc in self._accounts
            if acc.category_id == category_id
        ]

    def find_by_site(self, keyword: str) -> List[Account]:
        keyword = keyword.lower()
        return [
            acc for acc in self._accounts
            if keyword in acc.site.lower()
        ]

    def get_by_id(self, account_id: int) -> Account | None:
        for acc in self._accounts:
            if acc.id == account_id:
                return acc
        return None

    # Internal rules
    def _check_duplicate(self, new_account: Account):
        for acc in self._accounts:
            if (
                acc.site == new_account.site and
                acc.username == new_account.username
            ):
                raise ValueError(
                    "Ayni site ve username ile ikinci hesap eklenemez"
                )

    # Serialization helpers
    def to_list(self) -> list[dict]:
        return [acc.to_dict() for acc in self._accounts]

    @classmethod
    def from_list(cls, data: list[dict]) -> "Vault":
        accounts = [Account.from_dict(item) for item in data]
        return cls(accounts)
