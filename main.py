import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from services.storage_service import StorageService
from services.encryption_service import EncryptionService
from services.log_service import LogService
from services.search_service import SearchService

from controller.auth_controller import AuthController
from controller.vault_controller import VaultController
from controller.app_controller import AppController

from ui.login_screen import LoginScreen
from ui.dashboard import Dashboard
from ui.account_form import AccountForm

class SimpleValidator:
    def validate_master_password(self, password: str) -> bool:
        if len(password) < 4:
            raise ValueError("Master password en az 4 karakter olmalıdır.")
        return True

def main():

    app = QApplication(sys.argv)

    app.setApplicationName("LockLock")           
    app.setApplicationDisplayName("LockLock")    
    app.setOrganizationName("LockLock")

    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    icon_path = os.path.join(base_dir, "app_icon.jpeg") 

    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        if sys.platform == 'darwin':
             app.setWindowIcon(QIcon(icon_path))
    else:
        print(f"Uyarı: İkon dosyası bulunamadı: {icon_path}")

    user_data_dir = os.path.join(os.path.expanduser("~"), "Documents", "LockLock")
    os.makedirs(user_data_dir, exist_ok=True)
    
    db_path = os.path.join(user_data_dir, "app.db")

    storage = StorageService(db_path)
    storage.connect()
    
    schema_path = os.path.join(base_dir, "data", "schema.sql")
    if os.path.exists(schema_path):
        with open(schema_path, "r") as f:
            storage.conn.executescript(f.read())

    storage.execute("SELECT count(*) FROM categories")
    if storage.fetchone()[0] == 0:
        defaults = ["Social", "Work", "Finance", "Other", "Shopping", "Gaming"]
        for name in defaults:
            storage.execute("INSERT INTO categories (name, created_at) VALUES (?, ?)", 
                            (name, datetime.now().isoformat()), commit=True)

    logger = LogService(storage)
    encryption = EncryptionService(storage)
    search = SearchService(storage)
    validator = SimpleValidator()

    auth_controller = AuthController(encryption, storage, validator)
    vault_controller = VaultController(storage, encryption, search, logger)
    app_controller = AppController(auth_controller, vault_controller)

    login_window = LoginScreen()
    dashboard = Dashboard()
    
    def load_dashboard_data():
        try:
            total, cats = vault_controller.get_categories_for_dashboard()
            dashboard.update_categories(cats, total)
            
            accounts = vault_controller.list_accounts()
            dashboard.update_account_list(accounts)

        except Exception as e:
            print(f"Veri yükleme hatası: {e}")

    def handle_login(password):
        try:
            if auth_controller.is_first_run():
                auth_controller.setup_master_password(password)
                QMessageBox.information(login_window, "Başarılı", "Master Password oluşturuldu!")
            
            if app_controller.login(password):
                login_window.hide()
                load_dashboard_data()
                dashboard.show()
            else:
                login_window.show_error("Hatalı Master Password!")
        
        except ValueError as ve:
            login_window.show_error(str(ve))
        except Exception as e:
            login_window.show_error(f"Beklenmeyen hata: {e}")

    def on_search(keyword):
        if not keyword:
            load_dashboard_data()
            return
        results = vault_controller.search_accounts(keyword)
        dashboard.update_account_list(results)

    def on_category_selected(cat_id):
        if cat_id == 0:
            load_dashboard_data()
        else:
            results = vault_controller.list_by_category(cat_id)
            dashboard.update_account_list(results)

    def on_delete_account(acc_id):
        confirm = QMessageBox.question(
            dashboard, "Onay", 
            "Bu hesabı silmek istediğine emin misin?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            if vault_controller.delete_account(acc_id):
                load_dashboard_data()

    def on_copy_password(encrypted_pass):
        try:
            plain = encryption.decrypt(encrypted_pass)
            clipboard = QApplication.clipboard()
            clipboard.setText(plain)
        except Exception as e:
            QMessageBox.critical(dashboard, "Hata", f"Şifre çözülemedi: {e}")

    # --- HESAP EKLEME FONSİYONU ---
    def on_add_account_clicked():
        try:
            _, cat_objects = vault_controller.get_categories_for_dashboard()
            cat_list_for_form = [(c.id, c.name) for c in cat_objects]
            
            dlg = QDialog(dashboard)
            dlg.setWindowTitle("Add New Account")
            dlg.setFixedSize(400, 600)
            dlg.setStyleSheet("QDialog { background-color: white; }")

            layout = QVBoxLayout(dlg)
            layout.setContentsMargins(20, 20, 20, 20)
            
            form = AccountForm(cat_list_for_form) 
            layout.addWidget(form)
            
            btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
            btns.setStyleSheet(_get_btn_style())

            btns.accepted.connect(dlg.accept)
            btns.rejected.connect(dlg.reject)
            layout.addWidget(btns)
            
            if dlg.exec_() == QDialog.Accepted:
                data = form.get_data()
                vault_controller.add_account(
                    site=data["site"],
                    username=data["username"],
                    raw_password=data["password"],
                    category_id=data["category_id"]
                )
                load_dashboard_data()

        except Exception as e:
            QMessageBox.critical(dashboard, "Hata", str(e))

    # --- YENİ HESAP GÜNCELLEME FONSİYONU ---
    def on_edit_account_clicked(account):
        try:
            _, cat_objects = vault_controller.get_categories_for_dashboard()
            cat_list_for_form = [(c.id, c.name) for c in cat_objects]
            
            dlg = QDialog(dashboard)
            dlg.setWindowTitle("Edit Account")
            dlg.setFixedSize(400, 600)
            dlg.setStyleSheet("QDialog { background-color: white; }")

            layout = QVBoxLayout(dlg)
            layout.setContentsMargins(20, 20, 20, 20)
            
            form = AccountForm(cat_list_for_form)
            # Formu mevcut verilerle dolduruyoruz
            form.set_data(account)
            layout.addWidget(form)
            
            btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
            btns.setStyleSheet(_get_btn_style())

            btns.accepted.connect(dlg.accept)
            btns.rejected.connect(dlg.reject)
            layout.addWidget(btns)
            
            if dlg.exec_() == QDialog.Accepted:
                data = form.get_data()
                vault_controller.update_account(
                    account_id=account.id,
                    site=data["site"],
                    username=data["username"],
                    raw_password=data["password"], # Boşsa controller halledecek
                    category_id=data["category_id"]
                )
                load_dashboard_data()
                print("Hesap güncellendi.")

        except Exception as e:
            QMessageBox.critical(dashboard, "Hata", str(e))

    def _get_btn_style():
        return """
            QPushButton {
                height: 40px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                padding: 0 15px;
            }
            QPushButton[text="Save"] {
                background-color: #2563EB;
                color: white;
                border: none;
            }
            QPushButton[text="Save"]:hover {
                background-color: #1D4ED8;
            }
            QPushButton[text="Cancel"] {
                background-color: white;
                color: #374151;
                border: 1px solid #D1D5DB;
            }
            QPushButton[text="Cancel"]:hover {
                background-color: #F3F4F6;
            }
        """

    login_window.login_requested.connect(handle_login)
    dashboard.search_changed.connect(on_search)
    dashboard.category_selected.connect(on_category_selected)
    dashboard.delete_account_requested.connect(on_delete_account)
    dashboard.copy_password_requested.connect(on_copy_password)
    dashboard.add_account_clicked.connect(on_add_account_clicked)
    # Yeni sinyali bağla
    dashboard.edit_account_requested.connect(on_edit_account_clicked)

    if auth_controller.is_first_run():
        login_window.setWindowTitle("LockLock - Setup")
        login_window.login_button.setText("Create Master Key")
        login_window.password_input.setPlaceholderText("Create a strong master password...")
        login_window.show()
    else:
        login_window.show()
    
    exit_code = app.exec_()
    app_controller.shutdown()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()