![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green)
![Security](https://img.shields.io/badge/Encryption-AES--256-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

# LockLock

LockLock is a desktop-based password manager application focused on secure credential storage, authentication workflows, and security-oriented system design. The project emphasizes backend logic, cryptographic principles, and clean architecture rather than UI complexity.

This repository represents a learning-driven implementation of how password managers are built internally, with attention to correctness, maintainability, and security awareness.

---

## App Video

<video src="assets/ScreenRecordLockLock.mov" width="100%" controls></video>

---

## System Architecture

LockLock follows a layered and modular architecture where each responsibility is clearly isolated:

* **UI Layer (PyQt5)**
  Handles user interaction, form validation, and event handling. No sensitive logic is implemented at the UI level.

* **Application Controller**
  Manages application state transitions such as authentication, dashboard access, and secure session flow.

* **Security Layer**
  Responsible for encryption, key derivation, password verification, and secure data handling.

* **Data Layer**
  Manages local persistence, structured credential storage, and controlled data access.

This separation of concerns improves readability, testability, and future extensibility.

---

## Key Features

* **Military-Grade Encryption**
  All sensitive credential data is protected using symmetric encryption based on the `cryptography` library and Fernet (AES-128/256).

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

---

## Security Design Details

* Encryption keys are derived dynamically from the master password
* Raw passwords are never stored in plain text
* Sensitive operations require active authentication state
* Data access is strictly controlled through the application controller

The architecture is intentionally designed to be encryption-ready and adaptable to stronger cryptographic standards.

---

## Application ScreenShots

<img width="900" height="1378" alt="Screenshot 2026-01-11 at 11 34 11 PM_README" src="https://github.com/user-attachments/assets/96456868-7686-4d4c-8915-e0ca17b27862" />
<img width="900" height="623" alt="Screenshot 2026-01-11 at 11 36 24 PM_README" src="https://github.com/user-attachments/assets/fd06f1e8-599d-4a95-b060-d27ca3c430bc" />
<img width="434" height="650" alt="Screenshot 2026-01-14 at 1 26 44 PM" src="https://github.com/user-attachments/assets/039763fc-350b-4357-b75b-30487f5a3847" />

---

## Application Flow

1. Application startup
2. Master password setup or input
3. Key derivation and password verification
4. Secure dashboard access granted
5. Credential operations enabled
6. Application lock or exit

This flow enforces a single secure entry point to all sensitive data.

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
