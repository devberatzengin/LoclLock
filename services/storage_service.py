"""
    Tek basina SQLite ile konusan tek sey.

    Yapar:
        CRUD
        transaction
        migration (ileride)
        Model nesneleriyle calisir.
        Controller SQL gormez, model db gormez.
        
    """

import sqlite3
from pathlib import Path
from models.account import Account
import datetime

class StorageService():
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.conn: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    # Connection
    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    #Sql Executor
    def execute(self, query: str, params: tuple = (), commit: bool = False):
        try:
            self._cursor.execute(query, params)
            if commit:
                self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            raise e

    

    # Crud Operations

    def save_account(self, new_account: Account) -> int:
        query = """
            INSERT INTO accounts
            (site, username, encrypted_password, category_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        params = (
            new_account.site,
            new_account.username,
            new_account.encrypted_password,
            new_account.category_id,
            new_account.created_at.isoformat(),
            new_account.updated_at.isoformat()
        )

        self.execute(query, params, commit=True)
        return self.cursor.lastrowid

    def get_all_accounts(self) -> list[Account]:
        self.execute("SELECT * FROM accounts")
        
        rows = self.cursor.fetchall()

        accounts = []

        for row in rows:
            account = Account.from_row(row)
            accounts.append(account)
        
        return accounts
        
    def get_account_by_id(self, account_id: int) -> Account | None:
        query = "SELECT * FROM accounts WHERE id = ?"
        self.execute(query, (account_id,))

        row = self.cursor.fetchone()
        if row is None:
            return None

        return Account.from_row(row)
    
    def delete_account_by_id(self, account_id: int) -> bool:
        query = "DELETE FROM accounts WHERE id = ?"
        self.execute(query, (account_id,), commit=True)

        return self.cursor.rowcount > 0 #1 = Deleted, 0 = Not any match this id

    def update_account(self, account: Account) -> bool:
        query = """
        UPDATE accounts
        SET
            site = ?,
            username = ?,
            encrypted_password = ?,
            category_id = ?,
            updated_at = ?
        WHERE id = ?
        """

        params = (
            account.site,
            account.username,
            account.encrypted_password,
            account.category_id,
            datetime.datetime.now().isoformat(),
            account.id
        )

        self.execute(query, params, commit=True)

        return self.cursor.rowcount > 0
    
    def get_accounts_by_category_id(self,category_id:int) -> list[Account]:
        self.execute("SELECT * FROM accounts WHERE category_id = ?",(category_id))

        rows = self.cursor.fetchall()

        accounts = []

        for row in rows:
            account = Account.from_row(row)
            accounts.append(account)
    
        return accounts


    # Transaction Operations
    def begin_transaction(self):
        self._conn.execute("BEGIN")

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()


    #Log method
    def log(self, level: str, action: str, message: str):
        query = """
            INSERT INTO logs (level, action, message, created_at)
            VALUES (?, ?, ?, ?)
        """
        params = (
            level,
            action,
            message,
            datetime.datetime.now().isoformat()
        )
        self.execute(query, params)

    #Helpers
    def fetchone(self):
        return self.cursor.fetchone()
    
    def fetchall(self):
        return self.cursor.fetchall()