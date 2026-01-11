import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox

from services.storage_service import StorageService
from services.encryption_service import EncryptionService
from services.log_service import LogService
from services.search_service import SearchService

from controller.auth_controller import AuthController
from controller.vault_controller import VaultController
from controller.app_controller import AppController

from ui.login_screen import LoginScreen
from ui.dashboard import Dashboard
from ui.dialogs.add_account_dialog import AddAccountDialog
from ui.account_form import AccountForm

from models.category import Category  

class SimpleValidator:
    def validate_master_password(self, password: str) -> bool:
        if len(password) < 4:
            raise ValueError("Master password en az 4 karakter olmalıdır.")
        return True



def main():
    app = QApplication(sys.argv)
    
    # 1. Database Path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "data", "app.db")
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # 2. Start services
    storage = StorageService(db_path)

    storage.connect()
    with open(os.path.join(base_dir, "data", "schema.sql"), "r") as f:
        schema_sql = f.read()
        storage.conn.executescript(schema_sql) # type: ignore
    
    logger = LogService(storage)
    encryption = EncryptionService(storage)
    search = SearchService(storage)
    validator = SimpleValidator()

    # 3. Start controllers
    auth_controller = AuthController(encryption, storage, validator)
    vault_controller = VaultController(storage, encryption, search, logger)
    app_controller = AppController(auth_controller, vault_controller)

    # 4. Create Ui windows
    login_window = LoginScreen()
    dashboard = Dashboard()
    
    # ================= LOGIC & SIGNALS =================
    def handle_login(password):
        try:
            if auth_controller.is_first_run():
                auth_controller.setup_master_password(password)
                QMessageBox.information(login_window, "Başarılı", "Master Password oluşturuldu!")
            
            if app_controller.login(password):
                print("Giriş başarılı.")
                login_window.hide()
                load_dashboard_data()
                dashboard.show()
            else:
                login_window.show_error("Hatalı Master Password!")
        
        except ValueError as ve:
            login_window.show_error(str(ve))
        except Exception as e:
            login_window.show_error(f"Beklenmeyen hata: {e}")

    def load_dashboard_data():
        try:
            accounts = vault_controller.list_accounts()
            dashboard.update_account_list(accounts)

            total, cats = vault_controller.get_categories_for_dashboard()
            dashboard.update_categories(cats, total)
            
        except Exception as e:
            print(f"Veri yükleme hatası: {e}")

    # --- Dashboard Sinyalleri ---

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
            
            print("Şifre kopyalandı!") 
        except Exception as e:
            QMessageBox.critical(dashboard, "Hata", f"Şifre çözülemedi: {e}")

    def on_add_account_clicked():
        _, cat_objects = vault_controller.get_categories_for_dashboard()
        
        cat_list_for_form = [(c.id, c.name) for c in cat_objects]
        
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
        
        dlg = QDialog(dashboard)
        dlg.setWindowTitle("Add New Account")
        dlg.setFixedSize(400, 550)
        layout = QVBoxLayout(dlg)
        
        form = AccountForm(cat_list_for_form) 
        layout.addWidget(form)
        
        btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        layout.addWidget(btns)
        
        if dlg.exec_() == QDialog.Accepted:
            data = form.get_data()
            try:
                vault_controller.add_account(
                    site=data["site"],
                    username=data["username"],
                    raw_password=data["password"],
                    category_id=data["category_id"] 
                )
                load_dashboard_data() 
                print("Hesap eklendi.")
            except Exception as e:
                QMessageBox.critical(dashboard, "Hata", str(e))

    login_window.login_requested.connect(handle_login)
    
    dashboard.search_changed.connect(on_search)
    dashboard.category_selected.connect(on_category_selected)
    dashboard.delete_account_requested.connect(on_delete_account)
    dashboard.copy_password_requested.connect(on_copy_password)
    dashboard.add_account_clicked.connect(on_add_account_clicked)

    if auth_controller.is_first_run():
        login_window.setWindowTitle("LockLock - Setup")
        login_window.login_button.setText("Create Master Key")
        login_window.password_input.setPlaceholderText("Create a strong master password...")
    
    login_window.show()
  
    exit_code = app.exec_()
    app_controller.shutdown()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()