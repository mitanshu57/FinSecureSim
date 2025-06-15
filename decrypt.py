import os
from tkinter import messagebox
from cryptography.fernet import Fernet

def get_encryption_key():
    with open("key.key", 'rb') as key_file:
        return key_file.read()

def simulate_file_decryption(directory, key):
    encryption_key = get_encryption_key()
    cipher = Fernet(encryption_key)

    if key != encryption_key.decode():
        messagebox.showerror("Error", "Incorrect decryption key!")
        return False

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".encrypted"):
                file_path = os.path.join(root, file)
                original_file_path = file_path[:-10]

                # Read encrypted content and decrypt it
                with open(file_path, 'rb') as f:
                    encrypted_content = f.read()
                decrypted_content = cipher.decrypt(encrypted_content)

                # Rename file back to original and restore original content
                os.rename(file_path, original_file_path)
                with open(original_file_path, 'wb') as f:
                    f.write(decrypted_content)

    messagebox.showinfo("Success", "Files have been decrypted!")
    return True
