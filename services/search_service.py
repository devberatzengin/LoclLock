"""
    
    Arama mantigi.

    Yapar:
        keyword search
        kategori + keyword
        case-insensitive arama

    Avantaj:
        Yarin fuzzy search eklersin, hicbir seyi bozmaz.

"""

from models.account import Account

class SearchService():

    def __init__(self, storage):
        self.storage = storage

    def search_by_site(self, site_keyword: str) -> list[Account]:
        
        query = """
            SELECT * FROM accounts
            WHERE site LIKE ?
        """
        param = (f"%{site_keyword}%",)

        self.storage.execute(query, param)
        rows = self.storage.cursor.fetchall()

        return [Account.from_row(row) for row in rows]

    def search_by_username(self, username_keyword: str) -> list[Account]:
        
        query = """
            SELECT * FROM accounts
            WHERE username LIKE ?
        """
        param = (f"%{username_keyword}%",)

        self.storage.execute(query, param)
        rows = self.storage.cursor.fetchall()

        return [Account.from_row(row) for row in rows]
    
    def search_in_category(self, category_id: int, keyword: str) -> list[Account]:

        query = """
            SELECT * FROM accounts
            WHERE category_id = ?
            AND (site LIKE ? OR username LIKE ?)
        """

        params = (
            category_id,
            f"%{keyword}%",
            f"%{keyword}%"
        )

        self.storage.execute(query, params)
        rows = self.storage.cursor.fetchall()

        return [Account.from_row(row) for row in rows]

    def global_search(self, keyword: str) -> list[Account]:
        query = """
            SELECT * FROM accounts
            WHERE site LIKE ?
            OR username LIKE ?
        """

        param = (f"%{keyword}%", f"%{keyword}%")

        self.storage.execute(query, param)
        rows = self.storage.cursor.fetchall()

        return [Account.from_row(row) for row in rows]
