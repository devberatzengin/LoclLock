import hashlib
from models.account import Account
from models.category import Category

class VaultController:

    def __init__(self, storage_service, encryption_service, search_service, logger):
        self.storage = storage_service
        self.encryption = encryption_service
        self.search = search_service
        self.logger = logger
        self.is_locked = True

    def unlock_vault(self):
        self.is_locked = False

    def lock_vault(self):
        self.is_locked = True

    def cleanup(self):
        self.storage.close()

    def add_account(self, site, username, raw_password, category_id):
        if self.is_locked:
            raise PermissionError("Vault is locked")

        encrypted = self.encryption.encrypt(raw_password)
        
        account = Account(
            site=site,
            username=username,
            encrypted_password=encrypted,
            category_id=category_id
        )

        account_id = self.storage.save_account(account)
        self.logger.info("ACCOUNT_ADDED", f"id={account_id}")

        return account_id

    def update_account(self, account_id, site, username, raw_password, category_id):
        if self.is_locked:
            raise PermissionError("Vault is locked")

        existing_account = self.storage.get_account_by_id(account_id)
        if not existing_account:
            raise ValueError("Hesap bulunamadı!")

        if raw_password and raw_password.strip():
            final_encrypted_password = self.encryption.encrypt(raw_password)
        else:
            final_encrypted_password = existing_account.encrypted_password

        updated_account = Account(
            account_id=account_id,
            site=site,
            username=username,
            encrypted_password=final_encrypted_password,
            category_id=category_id,
            created_at=existing_account.created_at
        )

        success = self.storage.update_account(updated_account)
        if success:
            self.logger.info("ACCOUNT_UPDATED", f"id={account_id}")
        return success

    def delete_account(self, account_id: int) -> bool:
        if self.is_locked:
            raise PermissionError("Vault is locked")

        success = self.storage.delete_account_by_id(account_id)

        if success:
            self.logger.info("ACCOUNT_DELETED", f"id={account_id}")

        return success

    def list_accounts(self):
        if self.is_locked:
            raise PermissionError("Vault is locked")
        return self.storage.get_all_accounts()

    def list_by_category(self, category_id: int):
        if self.is_locked:
            raise PermissionError("Vault is locked")
        return self.storage.get_accounts_by_category_id(category_id)

    def get_categories_for_dashboard(self):
        rows = self.storage.get_categories_with_stats()
        total_count = self.storage.get_total_account_count()

        categories = []
        for row in rows:
            cat = Category(category_id=row[0], name=row[1])
            cat.count = row[2] 
            categories.append(cat)

        return total_count, categories

    def search_accounts(self, keyword: str):
        if self.is_locked:
            raise PermissionError("Vault is locked")
            
        results = self.search.global_search(keyword) 
        return results

    def change_master_key_and_reencrypt(self, old_key: bytes, new_key: bytes):
        if self.is_locked:
            raise PermissionError("Vault locked")

        try:
            self.logger.security("MASTER_KEY_CHANGE_START", "Re-encryption started")
            self.storage.begin_transaction()

            self.encryption.load_key(old_key)
            accounts = self.storage.get_all_accounts()
            decrypted = []

            for acc in accounts:
                plain = self.encryption.decrypt(acc.encrypted_password)
                decrypted.append((acc.id, plain))

            self.encryption.load_key(new_key)
            for acc_id, plain in decrypted:
                new_encrypted = self.encryption.encrypt(plain)
                self.storage.update_encrypted_password(acc_id, new_encrypted)

            key_hash = hashlib.sha256(new_key).hexdigest()
            self.storage.update_master_key_hash(key_hash)
            
            self.storage.commit()
            self.logger.security("MASTER_KEY_CHANGE_SUCCESS", "All passwords re-encrypted")

        except Exception as e:
            self.storage.rollback()
            self.logger.error("MASTER_KEY_CHANGE_FAILED", str(e))
            self.encryption.load_key(old_key) 
            raise