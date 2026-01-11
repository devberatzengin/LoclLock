"""
    
    Icermeli:
        id
        name
        icon (opsiyonel)

    Yapar:
        kategori kurallari
        duplicate kontrolu icin altyapi

    """

class Category:
    def __init__(
        self,
        name: str,
        category_id: int | None = None,
        icon: str | None = None
    ):
        self.id = category_id
        self.name = name
        self.icon = icon

        self.validate()

    # Validation
    def validate(self):
        if not self.name or not self.name.strip():
            raise ValueError("Category can't be null.")

        if len(self.name) < 2:
            raise ValueError("Category name have to be longer than 3 char.")

    # Serialization
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        return cls(
            category_id=data.get("id"),
            name=data["name"],
            icon=data.get("icon")
        )
