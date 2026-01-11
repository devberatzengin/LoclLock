from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QLineEdit,
    QFrame, QScrollArea, QApplication,
    QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.category_card import CategoryCard  # Özel widget'ımızı kullanıyoruz

class Dashboard(QWidget):
    # Sinyaller: Controller bu sinyalleri dinleyecek
    add_account_clicked = pyqtSignal()
    search_changed = pyqtSignal(str)
    category_selected = pyqtSignal(int)
    delete_account_requested = pyqtSignal(int)
    copy_password_requested = pyqtSignal(str) # Şifreli password'ü yollar

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LockLock - Vault Dashboard")
        self.resize(1200, 750)
        self.setStyleSheet("background-color: #F3F4F6;")
        
        # Verileri tutacağımız yerler
        self.category_widgets = []
        self._build_ui()

    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= SIDEBAR =================
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("background-color: #1F2937; border-right: 1px solid #374151;")
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(15)

        # Logo
        logo = QLabel("LockLock")
        logo.setStyleSheet("color: white; font-size: 24px; font-weight: 800; margin-bottom: 20px;")
        sidebar_layout.addWidget(logo)

        # Kategori Listesi (Scroll edilebilir)
        cat_scroll = QScrollArea()
        cat_scroll.setWidgetResizable(True)
        cat_scroll.setFrameShape(QFrame.NoFrame)
        cat_scroll.setStyleSheet("background: transparent; border: none;")
        
        self.cat_container = QWidget()
        self.cat_container.setStyleSheet("background: transparent;")
        self.cat_layout = QVBoxLayout(self.cat_container)
        self.cat_layout.setContentsMargins(0, 0, 0, 0)
        self.cat_layout.setSpacing(10)
        self.cat_layout.addStretch() # Kategorileri yukarı itmek için

        cat_scroll.setWidget(self.cat_container)
        sidebar_layout.addWidget(cat_scroll)
        
        # Alt Kısım (Versiyon vb.)
        version = QLabel("v1.0.0")
        version.setStyleSheet("color: #6B7280; font-size: 12px;")
        version.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(version)

        # ================= CONTENT =================
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(20)

        # --- Header (Search + Add Button) ---
        header = QHBoxLayout()
        
        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search accounts, usernames...")
        self.search_input.setFixedHeight(45)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #D1D5DB;
                border-radius: 10px;
                padding: 0 16px;
                font-size: 15px;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #2563EB;
            }
        """)
        self.search_input.textChanged.connect(self.search_changed.emit)

        # Add Button
        self.add_btn = QPushButton("+ New Account")
        self.add_btn.setFixedSize(140, 45)
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.clicked.connect(self.add_account_clicked.emit)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border-radius: 10px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)

        header.addWidget(self.search_input)
        header.addSpacing(15)
        header.addWidget(self.add_btn)

        # --- Accounts List (Scroll) ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                border: none;
                background: #E5E7EB;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #9CA3AF;
                border-radius: 4px;
            }
        """)

        self.cards_container = QWidget()
        self.cards_container.setStyleSheet("background: transparent;")
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setSpacing(15)
        self.cards_layout.setContentsMargins(0, 0, 10, 0) # Scrollbar için sağdan boşluk
        self.cards_layout.addStretch()

        self.scroll_area.setWidget(self.cards_container)

        content_layout.addLayout(header)
        content_layout.addWidget(self.scroll_area)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

    # ================= PUBLIC METHODS FOR CONTROLLER =================

    def update_categories(self, categories: list, total_count: int):

        while self.cat_layout.count():
            item = self.cat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.category_widgets = []

        # 1. "All Accounts" Kartı
        all_card = CategoryCard(0, "All Accounts", total_count)
        all_card.clicked.connect(self.handle_category_click)
        all_card.set_active(True)
        self.cat_layout.addWidget(all_card)
        self.category_widgets.append(all_card)

        # 2. Diğer Kategoriler
        for cat in categories:
            count = getattr(cat, 'count', 0) 
            card = CategoryCard(cat.id, cat.name, count) 
            card.clicked.connect(self.handle_category_click)
            self.cat_layout.addWidget(card)
            self.category_widgets.append(card)

        self.cat_layout.addStretch()

    def update_account_list(self, accounts: list):
        """
        Controller'dan gelen hesap listesiyle orta alanı günceller.
        accounts: List of Account objects
        """
        # Mevcut kartları temizle
        while self.cards_layout.count() > 1: # Stretch hariç
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Kart bulunamadıysa mesaj göster (Opsiyonel)
        if not accounts:
            lbl = QLabel("No accounts found.")
            lbl.setStyleSheet("color: #6B7280; font-size: 16px; margin-top: 20px;")
            lbl.setAlignment(Qt.AlignCenter)
            self.cards_layout.insertWidget(0, lbl)
            return

        # Hesapları ekle
        for acc in accounts:
            card = self._create_account_card(acc)
            self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)

    def _create_account_card(self, account):
        card = QFrame()
        card.setFixedHeight(80)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
            QFrame:hover {
                border: 1px solid #2563EB;
                background-color: #F9FAFB;
            }
        """)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(15)

        # Sol taraf: Bilgiler
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        site_lbl = QLabel(account.site)
        site_lbl.setStyleSheet("border: none; background: transparent; font-size: 16px; font-weight: 700; color: #111827;")
        
        user_lbl = QLabel(account.username)
        user_lbl.setStyleSheet("border: none; background: transparent; font-size: 13px; color: #6B7280;")

        info_layout.addWidget(site_lbl)
        info_layout.addWidget(user_lbl)

        # Sağ taraf: Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        # Copy Password Butonu
        copy_btn = QPushButton("Copy Pass")
        copy_btn.setFixedSize(90, 32)
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #EEF2FF;
                color: #4F46E5;
                border: 1px solid #C7D2FE;
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #E0E7FF; }
        """)
        # Lambda kullanarak account.encrypted_password verisini taşıyoruz
        copy_btn.clicked.connect(lambda: self.copy_password_requested.emit(account.encrypted_password))

        # Delete Butonu
        del_btn = QPushButton("Delete")
        del_btn.setFixedSize(70, 32)
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #DC2626;
                border: 1px solid #FECACA;
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #FEF2F2; }
        """)
        del_btn.clicked.connect(lambda: self.delete_account_requested.emit(account.id))

        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(del_btn)

        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addLayout(btn_layout)

        return card

    def handle_category_click(self, cat_id):
        # UI tarafında aktif olanı işaretle
        for widget in self.category_widgets:
            widget.set_active(widget.category_id == cat_id)
        
        # Controller'a haber ver
        self.category_selected.emit(cat_id)