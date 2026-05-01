# 🔐 Secure File Sharing System

A secure file sharing web application with virus scanning, end-to-end encryption, and password-protected downloads.

## ✨ Features

- **🛡️ VirusTotal Integration** - Automatic malware scanning before encryption
- **🔒 File Encryption** - Files are encrypted using Fernet (symmetric encryption)
- **🔑 Password Protection** - Each file has a unique download password
- **📤 Secure Sharing** - Generate encrypted shareable links
- **📊 Virus Scan Reports** - Direct links to detailed VirusTotal analysis

## 🏗️ Tech Stack

- **Backend**: Flask (Python)
- **Encryption**: Cryptography (Fernet)
- **Security**: VirusTotal API v3
- **Tunneling**: Ngrok (for external access)

## 📋 Prerequisites

- Python 3.8 or higher
- Ngrok account and binary (for external sharing)
- VirusTotal API key

## 🚀 Installation Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/secure-file-sharing.git
cd secure-file-sharing
Step 2: Create Virtual Environment
bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
bash
pip install flask requests cryptography
Step 4: Create Required Folders
bash
# Create uploads folder
mkdir uploads

# Create keys folder
mkdir keys

# Create static folder for images
mkdir static
Step 5: Add Static Images
Place the following images in the static/ folder:

hee.jpg - Background image for scanning and success pages

pass.jpg - Background image for password page

Step 6: Generate Encryption Key
Run the crypto_utils module to generate a key:

bash
python -c "from crypto_utils import generate_key; generate_key()"
This will create keys/key.key - Keep this file safe!

Step 7: Configure VirusTotal API
Edit app.py and replace the API key:

python
API_KEY = "your_virustotal_api_key_here"
Get a free API key from VirusTotal

Step 8: Setup Ngrok (Optional - for external sharing)
Download ngrok from ngrok.com

Extract ngrok.exe to your project folder

Run ngrok to expose your local server:

bash
# In a separate terminal
ngrok http 5000
🎯 Running the Application
Start Flask Application
bash
python app.py
Access the Application
Local Access: http://127.0.0.1:5000

External Access: Use the ngrok URL (e.g., https://your-ngrok-url.ngrok.io)

📁 Project Structure
text
secure-file-sharing/
│
├── app.py                 # Main Flask application
├── crypto_utils.py        # Encryption/decryption utilities
├── main.py               # Database initialization (optional)
│
├── uploads/              # Uploaded files (created automatically)
├── keys/                 # Encryption keys folder
│   └── key.key          # Generated encryption key
├── static/               # Static assets
│   ├── hee.jpg          # Background images
│   └── pass.jpg
│
├── templates/            # HTML templates
│   ├── upload.html
│   ├── scanning.html
│   ├── success.html
│   └── password.html
│
└── database.db          # SQLite database (auto-created)
🔄 How It Works
Upload: User uploads a file with a password

Scan: File is scanned via VirusTotal API

Encryption: If safe, file is encrypted using Fernet

Sharing: System generates a secure download link

Download: Recipient enters password, file is decrypted

⚠️ Security Notes
The encryption key (keys/key.key) is critical - never share it

Passwords are stored temporarily in memory (not persistent)

Files are deleted if malware is detected

Consider implementing a database for production use

🛠️ Troubleshooting
Issue: "No module named cryptography"
bash
pip install cryptography
Issue: "keys/key.key not found"
bash
mkdir keys
python -c "from crypto_utils import generate_key; generate_key()"
Issue: Ngrok URL not working
Ensure ngrok is running on port 5000

Check ngrok status: http://127.0.0.1:4040/api/tunnels

Issue: VirusTotal API rate limit
Free API key has limits (~4 requests per minute)

Consider upgrading or adding delays

📝 Future Improvements
User authentication system

Persistent password storage with database

File expiration feature

Multiple file uploads

Email notifications

Download tracking and analytics

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
VirusTotal for malware scanning API

Flask for web framework

Cryptography.io for encryption libraries

📧 Contact
For questions or support, please open an issue on GitHub.
