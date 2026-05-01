from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()

    with open("keys/key.key", "wb") as f:
        f.write(key)

from cryptography.fernet import Fernet

def load_key():
    return open("keys/key.key", "rb").read()


def encrypt_file(file_path):
    key = load_key()
    cipher = Fernet(key)

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted = cipher.encrypt(data)

    with open(file_path, "wb") as f:
        f.write(encrypted)


def decrypt_file(file_path):
    key = load_key()
    cipher = Fernet(key)

    with open(file_path, "rb") as f:
        data = f.read()

    decrypted = cipher.decrypt(data)

    with open(file_path, "wb") as f:
        f.write(decrypted)