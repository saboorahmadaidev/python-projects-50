from cryptography.fernet import Fernet
import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "key.key")
PASSWORD_PATH = os.path.join(BASE_DIR, "passwords.txt")



def write_key():
    """Generate and save a new encryption key."""
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)


def load_key():
    """Load existing key or create one if missing."""
    if not os.path.exists(KEY_PATH):
        write_key()

    with open(KEY_PATH, "rb") as f:
        return f.read()


key = load_key()
fer = Fernet(key)




def view_passwords():
    """Decrypt and display stored passwords."""
    if not os.path.exists(PASSWORD_PATH):
        print("\nNo passwords stored yet.\n")
        return

    print("\nStored Accounts:\n" + "-" * 30)

    with open(PASSWORD_PATH, "r") as f:
        lines = f.readlines()

        if not lines:
            print("No saved accounts.\n")
            return

        for line in lines:
            line = line.strip()
            if not line:
                continue

            try:
                user, encrypted_pwd = line.split("|", 1)
                decrypted_pwd = fer.decrypt(encrypted_pwd.encode()).decode()
                print(f"Account: {user}")
                print(f"Password: {decrypted_pwd}")
                print("-" * 30)

            except Exception:
                print("⚠ Skipping corrupted or undecryptable entry.\n")


def add_password():
    """Encrypt and store a new password."""
    name = input("Account Name: ").strip()
    pwd = input("Password: ").strip()

    if not name or not pwd:
        print("Account name and password cannot be empty.\n")
        return

    encrypted_pwd = fer.encrypt(pwd.encode()).decode()

    with open(PASSWORD_PATH, "a") as f:
        f.write(f"{name}|{encrypted_pwd}\n")

    print("✅ Password added successfully.\n")

def main():
    print("=== Secure Password Manager ===")

    while True:
        mode = input(
            "\nChoose: add | view | q (quit): "
        ).lower().strip()

        if mode == "q":
            print("Goodbye 👋")
            sys.exit()

        elif mode == "view":
            view_passwords()

        elif mode == "add":
            add_password()

        else:
            print("Invalid option. Please choose add, view, or q.\n")


if __name__ == "__main__":
    main()
