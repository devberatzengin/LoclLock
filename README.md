<<<<<<< HEAD
# LockLock
=======
# 🔒 LockLock

**LockLock**, verilerinizi bulutta değil, kendi cihazınızda şifreli olarak saklayan, modern arayüze sahip, güvenli ve açık kaynaklı bir parola yöneticisidir.
>>>>>>> 8789ee6a088bc59e37d07d6175014a4d9e62664c

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green)
![Security](https://img.shields.io/badge/Encryption-AES--256-red)

LockLock is a desktop-based password manager application focused on secure credential storage, authentication workflows, and security-oriented system design. The project emphasizes backend logic, cryptographic principles, and clean architecture rather than UI complexity.

This repository represents a learning-driven implementation of how password managers are built internally, with attention to correctness, maintainability, and security awareness.

---

## System Architecture

<<<<<<< HEAD
LockLock follows a layered and modular architecture where each responsibility is clearly isolated:
=======
LockLock, "Önce Güvenlik" ve "Modern UX" prensipleriyle geliştirilmiştir. Kullanıcıların hassas verilerini (şifreler, notlar) **AES-256** standardı ile şifreler ve bu verilere erişim sadece kullanıcının belirlediği **Master Password (Ana Şifre)** ile mümkündür.
>>>>>>> 8789ee6a088bc59e37d07d6175014a4d9e62664c

* **UI Layer (PyQt5)**
  Handles user interaction, form validation, and event handling. No sensitive logic is implemented at the UI level.

<<<<<<< HEAD
* **Application Controller**
  Manages application state transitions such as authentication, dashboard access, and secure session flow.
=======
## 📸 Ekran Görüntüleri

* ** Giriş Ekranı ***
<img width="399" height="611" alt="Screenshot 2026-01-11 at 11 34 11 PM" src="https://github.com/user-attachments/assets/f7d0b252-fcaa-4905-8831-ca06e0a1c630" />

* ** Dashboard Ekranı **
<img width="1204" height="834" alt="Screenshot 2026-01-11 at 11 36 24 PM" src="https://github.com/user-attachments/assets/1f8d1e63-ff6c-48c2-be18-10ffd0f2cf83" />

* ** Add New Account Ekranı **
<img width="404" height="638" alt="Screenshot 2026-01-11 at 11 39 33 PM" src="https://github.com/user-attachments/assets/9dbd71bf-b0eb-4393-9948-25bc9c9eaa0f" />

## ✨ Özellikler
>>>>>>> 8789ee6a088bc59e37d07d6175014a4d9e62664c

* **Security Layer**
  Responsible for encryption, key derivation, password verification, and secure data handling.

* **Data Layer**
  Manages local persistence, structured credential storage, and controlled data access.

This separation of concerns improves readability, testability, and future extensibility.

---

## Key Features

<<<<<<< HEAD
* **Military-Grade Encryption**
  All sensitive credential data is protected using symmetric encryption based on the `cryptography` library and Fernet (AES-128/256).
=======
1.  **Repoyu klonlayın:**
    ```bash
    git clone [https://github.com/kullaniciadiniz/LockLock.git](https://github.com/kullaniciadiniz/LockLock.git)
    cd LockLock
    ```
>>>>>>> 8789ee6a088bc59e37d07d6175014a4d9e62664c

* **Secure Key Derivation**
  The master password is never stored directly. Instead, `PBKDF2HMAC` with `SHA256` is used along with a unique per-user salt to derive secure encryption keys.

* **Authentication-Centered Design**
  Access to all credential operations is strictly gated behind successful master password verification.

* **Modern Desktop UI**
  Built with PyQt5, featuring a clean dark-mode interface and intuitive navigation focused on usability.

* **Credential Categorization**
  Stored accounts can be grouped into categories such as Social, Work, or Finance, enabling better organization and clarity.

* **Fast Access Operations**
  One-click password copy, credential edit, and secure deletion workflows.

* **Smart Search**
  Instant filtering of credentials by site name or username for quick access.

* **Fully Local Storage**
  No data is transmitted or stored remotely. All credentials remain on the local machine under user control.

<<<<<<< HEAD
---
=======
LockLock, sürdürülebilirlik, test edilebilirlik ve modülerlik ilkeleri gözetilerek **Model-View-Controller (MVC)** mimarisi üzerine inşa edilmiştir. Ayrıca "Service Layer" (Servis Katmanı) yaklaşımı ile iş mantığı veritabanı işlemlerinden izole edilmiştir.
>>>>>>> 8789ee6a088bc59e37d07d6175014a4d9e62664c

## Security Design Details

* Encryption keys are derived dynamically from the master password
* Raw passwords are never stored in plain text
* Sensitive operations require active authentication state
* Data access is strictly controlled through the application controller

The architecture is intentionally designed to be encryption-ready and adaptable to stronger cryptographic standards.

---

## Application Flow

1. Application startup
2. Master password setup or input
3. Key derivation and password verification
4. Secure dashboard access granted
5. Credential operations enabled
6. Application lock or exit

This flow enforces a single secure entry point to all sensitive data.

<<<<<<< HEAD
---

## Technologies Used

* Programming Language: Python
* UI Framework: PyQt5
* Cryptography: cryptography (Fernet, PBKDF2HMAC, SHA256)
* Architecture: Modular layered design
* Version Control: Git

---

## Concepts Practiced

* Cryptographic fundamentals
* Authentication and access control
* Secure local data storage
* Modular software architecture
* State management in desktop applications

---

## Disclaimer

This project is built strictly for educational purposes. It is not intended for production use without additional security hardening, formal audits, and advanced key management strategies.

---

## Author

**Berat Zengin**

* GitHub: [https://github.com/devberatzengin](https://github.com/devberatzengin)
* LinkedIn: [https://linkedin.com/in/berat-zengin-1a337a294](https://linkedin.com/in/berat-zengin-1a337a294)
=======
```plaintext
LockLock/
├── controller/        # İş Mantığı (Business Logic)
│   ├── app_controller.py   # Uygulama yaşam döngüsü ve giriş kontrolü
│   ├── auth_controller.py  # Master password doğrulama işlemleri
│   └── vault_controller.py # Hesap ekleme, silme, listeleme mantığı
├── models/            # Veri Objeleri (Data Transfer Objects)
├── services/          # Çekirdek Servisler (Core Services)
│   ├── encryption_service.py # AES-256 & PBKDF2 mantığı
│   ├── storage_service.py    # SQLite Wrapper
│   └── search_service.py     # Arama algoritmaları
├── ui/                # Görsel Arayüz (GUI)
├── data/              # Veritabanı (app.db)
└── main.py            # Uygulama Başlatıcısı (Entry Point)
>>>>>>> 8789ee6a088bc59e37d07d6175014a4d9e62664c
