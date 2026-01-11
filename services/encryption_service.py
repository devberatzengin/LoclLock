"""
Guvenligin kalbi.

    Sorumluluklari:
        encrypt
        decrypt
        key derivation
        master password handling

    Bilmesi gereken:
        config.json

    Bilmemesi gereken:
        UI
        SQL

"""
import json
import base64
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend


CONFIG_PATH = Path("/Users/beratzengin/Desktop/Github/LoclLock/data/config.json")


class EncryptionService():
    def __init__(self):
        self.config = self._load_config()
        self.backend = default_backend()

    # Config
    def _load_config(self) -> dict:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    # Key derivation
    def derive_key(self, master_password: str, salt: bytes) -> bytes:
        enc_cfg = self.config["encryption"]
        kdf_cfg = enc_cfg["kdf"]

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=kdf_cfg["key_length"],
            salt=salt,
            iterations=kdf_cfg["iterations"],
            backend=self.backend
        )

        return base64.urlsafe_b64encode(
            kdf.derive(master_password.encode(enc_cfg["encoding"]))
        )

    # Encryption / Decryption
    def encrypt(self, plain_text: str, key: bytes) -> str:
        if len(plain_text) < 8:
            raise ValueError("Password must be at least 8 characters")

        fernet = Fernet(key)
        encrypted = fernet.encrypt(plain_text.encode())
        return encrypted.decode()

    def decrypt(self, encrypted_text: str, key: bytes) -> str:
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_text.encode())
        return decrypted.decode()
