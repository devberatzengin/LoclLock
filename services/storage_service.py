import sqlite3
from pathlib import Path
from datetime import datetime

# Yeni modelimizi import ediyoruz
from models.account import Account

class StorageService:
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.conn: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def execute(self, query, params=(), commit=False):
        try:
            self.cursor.execute(query, params)
            if commit:
                self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def save_account(self, new_account: Account) -> int:
        try:
            self.begin_transaction()

            query = """
                INSERT INTO accounts
                (site, username, encrypted_password, category_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            # Nesnenin kendi propertylerini kullanıyoruz
            self.execute(query, new_account.to_db_params())
            
            account_id = self.cursor.lastrowid

            self.log(
                level="INFO",
                action="CREATE_ACCOUNT",
                message=f"Account created with id={account_id}"
            )

            self.commit()
            return account_id

        except Exception as e:
            self.rollback()
            self.log(
                level="ERROR",
                action="CREATE_ACCOUNT",
                message=str(e)
            )
            self.commit()
            raise

    def get_all_accounts(self) -> list[Account]:
        self.execute("SELECT * FROM accounts")
        rows = self.cursor.fetchall()
        return [Account.from_row(row) for row in rows]
        
    def get_account_by_id(self, account_id: int) -> Account | None:
        try:
            query = "SELECT * FROM accounts WHERE id = ?"
            self.execute(query, (account_id,))
            row = self.cursor.fetchone()

            if row is None:
                return None

            return Account.from_row(row)

        except Exception as e:
            self.log(
                level="ERROR",
                action="GET_ACCOUNT_BY_ID",
                message=str(e)
            )
            self.commit()
            raise

    def delete_account_by_id(self, account_id: int) -> bool:
        try:
            self.begin_transaction()

            query = "DELETE FROM accounts WHERE id = ?"
            self.execute(query, (account_id,))
            deleted = self.cursor.rowcount > 0 

            if deleted:
                self.log(level="INFO", action="DELETE_ACCOUNT", message=f"Account deleted id={account_id}")
            else:
                self.log(level="INFO", action="DELETE_ACCOUNT", message=f"No account found for id={account_id}")

            self.commit()
            return deleted

        except Exception as e:
            self.rollback()
            self.log(level="ERROR", action="DELETE_ACCOUNT", message=str(e))
            self.commit()
            raise

    def update_account(self, account: Account) -> bool:
        try:
            self.begin_transaction()

            query = """
            UPDATE accounts
            SET site = ?, username = ?, encrypted_password = ?, category_id = ?, updated_at = ?
            WHERE id = ?
            """
            params = (
                account.site,
                account.username,
                account.encrypted_password,
                account.category_id,
                datetime.now().isoformat(),
                account.id
            )

            self.execute(query, params)
            updated = self.cursor.rowcount > 0

            if updated:
                self.log(level="INFO", action="UPDATE_ACCOUNT", message=f"Account updated id={account.id}")

            self.commit()
            return updated

        except Exception as e:
            self.rollback()
            self.log(level="ERROR", action="UPDATE_ACCOUNT", message=str(e))
            self.commit()
            raise

    def get_accounts_by_category_id(self, category_id: int) -> list[Account]:
        self.execute("SELECT * FROM accounts WHERE category_id = ?", (category_id,))
        rows = self.cursor.fetchall()
        return [Account.from_row(row) for row in rows]

    def update_encrypted_password(self, account_id: int, encrypted: str):
        query = """
        UPDATE accounts
        SET encrypted_password = ?, updated_at = datetime('now')
        WHERE id = ?
        """
        self.execute(query, (encrypted, account_id))

    def update_master_key_hash(self, new_key: str):
        query = """
        INSERT OR REPLACE INTO meta (key, value)
        VALUES ('master_key_hash', ?)
        """
        self.execute(query, (new_key,), commit=False)

    def begin_transaction(self):
        self.conn.execute("BEGIN")

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def has_master_key(self) -> bool:
        self.execute("SELECT 1 FROM meta WHERE key = 'master_key_hash'")
        return self.cursor.fetchone() is not None

    def save_master_key_meta(self, salt: str, key_hash: str):
        self.begin_transaction()
        self.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES ('master_key_salt', ?), ('master_key_hash', ?)",
            (salt, key_hash)
        )
        self.commit()

    def get_master_key_meta(self) -> dict | None:
        self.execute("SELECT key, value FROM meta WHERE key IN ('master_key_salt', 'master_key_hash')")
        rows = self.cursor.fetchall()
        return {key: value for key, value in rows} if rows else None

    def log(self, level: str, action: str, message: str):
        query = "INSERT INTO logs (action, detail, level, created_at) VALUES (?, ?, ?, ?)"
        # message parametresi 'detail' sütununa kaydediliyor
        params = (action, message, level, datetime.now().isoformat())
        self.execute(query, params)

    def fetchone(self):
        return self.cursor.fetchone()
    
    def fetchall(self):
        return self.cursor.fetchall()