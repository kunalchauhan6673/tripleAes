# 🔐 Secure File System (Triple AES Encryption)

A Python-based secure file encryption system with GUI, login/signup authentication, and multi-layer AES encryption.

---

## 🚀 Features

- 🔐 Triple-layer AES encryption (CBC mode)
- 👤 Login & Signup system (hashed passwords)
- 📂 Supports ALL file types (images, PDFs, videos, etc.)
- 🖼 Image preview (only for non-encrypted images)
- 🚫 Auto-hide preview for encrypted files
- 🔑 Optional encryption using account credentials
- 📊 Progress bar for operations
- 🖥 User-friendly GUI using Tkinter

---

## 🛠 Tech Stack

- Python
- Tkinter (GUI)
- PyCryptodome (Encryption)
- Pillow (Image preview)

---

## 📁 Project Structure
tripleAes/
│── main.py
│── gui.py
│── crypto_utils.py
│── auth.py
│── users.json (ignored)
│── .gitignore
│── README.md


---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/kunalchauhan6673/tripleAes.git
cd tripleAes

2. Install dependencies
pip install pycryptodome pillow

▶️ Run the Application
python main.py

🔐 How It Works
Files are encrypted using 3 layers of AES encryption
Keys are derived using PBKDF2
Data integrity is verified using SHA-256 hashing
Users can optionally use their account credentials as encryption key
💡 Future Improvements
🔑 Cloud key management (AWS Secrets Manager)
📂 Drag & drop file support
👨‍💻 Author

Kunal Chauhan
