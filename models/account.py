"""
    Icermeli:
        site
        username
        encrypted_password
        category_id
        timestamps

    Yapar:
        kendini validate edebilir
        serialize / deserialize

    Yapmaz:
        SQL baglantisi
        encryption

    """

from datetime import datetime

class Account:
    
    #Constructor
    def __init__(
        self,
        site: str,
        username: str,
        encrypted_password: str,
        category_id: int,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        account_id: int | None = None
    ):
        self.id = account_id
        self.site = site
        self.username = username
        self.encrypted_password = encrypted_password
        self.category_id = category_id

        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

        self.validate()


    # Validation
    def validate(self):
        if not self.site or not self.site.strip():
            raise ValueError("Site can't be null.")

        if not self.username or not self.username.strip():
            raise ValueError("Username can't be null.")

        if not self.encrypted_password:
            raise ValueError("Encrypted password can't be null.")

        if not isinstance(self.category_id, int):
            raise ValueError("Category id must be an integer.")

    # Serialization
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "site": self.site,
            "username": self.username,
            "encrypted_password": self.encrypted_password,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        return cls(
            account_id=data.get("id"),
            site=data["site"],
            username=data["username"],
            encrypted_password=data["encrypted_password"],
            category_id=data["category_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    # Utilities
    def touch(self):
        self.updated_at = datetime.now()
