# 🔒 LockLock

**LockLock**, verilerinizi bulutta değil, kendi cihazınızda şifreli olarak saklayan, modern arayüze sahip, güvenli ve açık kaynaklı bir parola yöneticisidir.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green)
![Security](https://img.shields.io/badge/Encryption-AES--256-red)

---

## 📖 Proje Hakkında

LockLock, "Önce Güvenlik" ve "Modern UX" prensipleriyle geliştirilmiştir. Kullanıcıların hassas verilerini (şifreler, notlar) **AES-256** standardı ile şifreler ve bu verilere erişim sadece kullanıcının belirlediği **Master Password (Ana Şifre)** ile mümkündür.

Veritabanı olarak **SQLite** kullanılır ancak veriler veritabanına yazılmadan *önce* şifrelenir. Bu sayede veritabanı dosyası (`app.db`) çalınsa bile içerisindeki veriler ana şifre olmadan anlamsızdır.

## 📸 Ekran Görüntüleri

* ** Giriş Ekranı ***
<img width="399" height="611" alt="Screenshot 2026-01-11 at 11 34 11 PM" src="https://github.com/user-attachments/assets/f7d0b252-fcaa-4905-8831-ca06e0a1c630" />

* ** Dashboard Ekranı **
<img width="1204" height="834" alt="Screenshot 2026-01-11 at 11 36 24 PM" src="https://github.com/user-attachments/assets/1f8d1e63-ff6c-48c2-be18-10ffd0f2cf83" />

* ** Add New Account Ekranı **
<img width="404" height="638" alt="Screenshot 2026-01-11 at 11 39 33 PM" src="https://github.com/user-attachments/assets/9dbd71bf-b0eb-4393-9948-25bc9c9eaa0f" />

## ✨ Özellikler

* **🛡️ Askeri Düzeyde Şifreleme:** Veriler `cryptography` kütüphanesi kullanılarak Fernet (AES-128/256) simetrik şifreleme ile korunur.
* **🔑 Güvenli Anahtar Türetme:** Ana şifreniz asla kaydedilmez. Bunun yerine `PBKDF2HMAC` ve `SHA256` kullanılarak her kullanıcı için benzersiz bir `salt` ile hash'lenir.
* **🎨 Modern & Responsive UI:** PyQt5 ile geliştirilmiş, göz yormayan, "Dark Mode" destekli yan menü ve kategori bazlı renk kodlamasına sahip modern arayüz.
* **📂 Kategorizasyon:** Hesaplarınızı (Sosyal, İş, Finans vb.) kategorilere ayırın. Her kategori otomatik olarak renklenir.
* **⚡ Hızlı Erişim:** Tek tıkla şifre kopyalama, hesap düzenleme ve silme.
* **🔍 Akıllı Arama:** Hesaplarınız arasında site adı veya kullanıcı adına göre anında arama yapın.
* **🏠 %100 Yerel:** Hiçbir veri internete yüklenmez. Tüm kontrol sizde.

## 🛠️ Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler
* Python 3.10 veya üzeri
* pip

### Adım Adım Kurulum

1.  **Repoyu klonlayın:**
    ```bash
    git clone [https://github.com/kullaniciadiniz/LockLock.git](https://github.com/kullaniciadiniz/LockLock.git)
    cd LockLock
    ```

2.  **Sanal ortam oluşturun (Önerilen):**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Bağımlılıkları yükleyin:**
    ```bash
    pip install PyQt5 cryptography
    ```

4.  **Uygulamayı başlatın:**
    ```bash
    python main.py
    ```

## 🚀 Kullanım

1.  **İlk Kurulum:** Uygulamayı ilk açtığınızda sizden bir **Master Password** belirlemeniz istenir. Bu şifreyi unutursanız verilerinize erişemezsiniz!
2.  **Giriş:** Belirlediğiniz şifre ile kasanın kilidini açın.
3.  **Hesap Ekleme:** `+ New Account` butonuna tıklayın. Site, kullanıcı adı, şifre ve kategori bilgilerini girin.
4.  **Kategoriler:** Sol menüden kategorilere tıklayarak filtreleme yapın. Kartların kenar renkleri kategoriye göre değişecektir (Örn: Finans için Yeşil, Sosyal için Mavi).

## 🏗️ Teknik Mimari ve Tasarım Desenleri

LockLock, sürdürülebilirlik, test edilebilirlik ve modülerlik ilkeleri gözetilerek **Model-View-Controller (MVC)** mimarisi üzerine inşa edilmiştir. Ayrıca "Service Layer" (Servis Katmanı) yaklaşımı ile iş mantığı veritabanı işlemlerinden izole edilmiştir.

### Mimari Katmanlar (MVC Breakdown)

Proje 4 ana katmandan oluşur:

* **🟦 Model (Veri Katmanı - `models/`):**
    * Uygulamanın veri iskeletini oluşturur (`Account`, `Category`, `Log`).
    * Saf Python sınıflarıdır; veritabanı bağlantısı veya UI kodu içermezler.
    * Veri doğrulama (Validation) işlemleri (örn: şifre boş olamaz) burada yapılır.
    * *Örnek:* `Account` sınıfı, bir hesabın şifreli parolasını ve oluşturulma tarihini tutar.

* **🟪 View (Arayüz Katmanı - `ui/`):**
    * Kullanıcının gördüğü PyQt5 pencereleridir (`Dashboard`, `LoginScreen`).
    * İş mantığı barındırmazlar (Dumb UI). Sadece veriyi gösterir ve kullanıcı girdilerini **Sinyaller (Signals)** aracılığıyla Controller'a iletirler.
    * CSS benzeri QSS (Qt Style Sheets) ile modernize edilmiştir.

* **🟧 Controller (Kontrol Katmanı - `controller/`):**
    * Uygulamanın "beyni"dir. View ile Model/Service arasındaki iletişimi yönetir.
    * View'dan gelen sinyalleri (örn: "Kaydet butonuna basıldı") yakalar, veriyi işler ve sonucu tekrar View'a gönderir.
    * *Örnek:* `VaultController`, arayüzden gelen ham şifreyi alır, `EncryptionService`'e şifreletir ve `StorageService`'e kaydettirir.

* **🟩 Service (Servis Katmanı - `services/`):**
    * Tekrar kullanılabilir, düşük seviyeli işlemleri yapan yardımcı sınıflardır.
    * **EncryptionService:** Şifreleme/Çözme ve Anahtar Türetme işlemlerini yönetir.
    * **StorageService:** SQLite veritabanı ile konuşan tek katmandır (SQL sorguları sadece buradadır).

### Dizin Yapısı

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
