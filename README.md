# PhantomCrypt Simulator

A safe and non-destructive ransomware behavior simulator for testing security measures and raising user awareness.

## 🚀 Project Overview

PhantomCrypt Simulator mimics the behavior of real-world ransomware without causing any permanent damage. It encrypts designated test files, displays a ransom note with a countdown timer, and simulates disabled functionalities. All operations are reversible to ensure that your data remains intact.

## 🔑 Key Features

- **Symmetric File Encryption/Decryption**: Utilizes AES encryption to secure files and renames them to indicate their encrypted state.
- **Ransom Note GUI**: Presents a graphical ransom note with instructions, a countdown timer, and a field to enter the decryption key.
- **Non-Destructive Workflow**: Every encryption operation can be reversed to restore files to their original state.
- **Simulation Mode**: Emulates the full lifecycle of a ransomware attack without any real damage.

## 🛠️ Tools & Technologies

- **Language:** Python 3.8+
- **Libraries & Frameworks:**
  - `PyCryptodome` for AES encryption and decryption
  - `os`, `shutil` for file and directory operations
  - `Tkinter` for building the ransom note window
  - `Pillow` for handling GUI images
- **Development Environment:** Visual Studio Code

## 📦 Installation & Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/phantomcrypt-simulator.git
   cd phantomcrypt-simulator
