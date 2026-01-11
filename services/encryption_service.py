import os
import base64
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

class EncryptionService:

    def __init__(self, storage_service):
        self._key: bytes | None = None
        self.storage = storage_service

    # Key derivation
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=200_000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(
            kdf.derive(password.encode())
        )

    # First run
    def create_master_key(self, password: str):
        if len(password) < 8:
            raise ValueError("Master password must be at least 8 chars")

        salt = os.urandom(16)
        key = self._derive_key(password, salt)

        key_hash = hashlib.sha256(key).hexdigest()

        self.storage.save_master_key_meta(
            salt=salt.hex(),
            key_hash=key_hash
        )

        self._key = key

    # Login - HATA BURADAYDI, DÜZELTİLDİ
    def verify_master_key(self, password: str) -> bool:
        meta = self.storage.get_master_key_meta()
        if not meta:
            return False

        # Veritabanından gelen anahtarlar 'master_key_salt' ve 'master_key_hash'
        try:
            salt_hex = meta["master_key_salt"]
            salt = bytes.fromhex(salt_hex)
            expected_hash = meta["master_key_hash"]
        except KeyError:
            # Eğer anahtarlar eksikse false dön
            return False

        key = self._derive_key(password, salt)
        key_hash = hashlib.sha256(key).hexdigest()

        if key_hash != expected_hash:
            return False

        self._key = key
        return True

    # Runtime usage
    def load_key(self, key: bytes):
        if not key:
            raise ValueError("Key cannot be empty")
        self._key = key

    def encrypt(self, plain_text: str) -> str:
        if not self._key:
            raise RuntimeError("Vault is locked")

        fernet = Fernet(self._key)
        return fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, cipher_text: str) -> str:
        if not self._key:
            raise RuntimeError("Vault is locked")

        fernet = Fernet(self._key)
        return fernet.decrypt(cipher_text.encode()).decode()

    # Utils
    def clear_key(self):
        self._key = None