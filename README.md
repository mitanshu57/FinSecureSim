
## Project Overview

The project aims to develop a ransomware simulator that mimics the behavior of actual ransomware without causing any harm. The simulator encrypts test files, displays a ransom note, and simulates disabling functionalities to test security measures and user awareness.

### Key Features
- **File Encryption/Decryption**: The simulator encrypts files using symmetric encryption (AES) and renames them to show their encrypted state.
- **Ransom Note GUI**: A graphical window displays the ransom message with a countdown timer and fields for the decryption key.
- **Non-Destructive**: The encryption and decryption operations are reversible to prevent data loss.

## Tools and Technologies Used

- **Programming Language**: Python
- **Libraries and Frameworks**:
  - **Cryptography**: `PyCryptodome` for encryption and decryption
  - **File Manipulation**: `os` and `shutil` for file and directory operations
  - **GUI Development**: `Tkinter` for building the ransom note window
  - **Image Processing**: `Pillow` for image handling in the GUI
- **Development Environment**: Visual Studio Code (VS Code)

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ransomeware_simulation.git
   cd ransomeware_simulation
2. Install required Python libraries:
   ```bash
   pip install -r requirements.txt
3. Run the encryption script:
   ```bash
   python script.py
4. Enter the decryption key from the key.key file when prompted by the ransom note window to decrypt the files.

## How It Works
1. File Encryption:
- The simulator encrypts files in the specified directory using the AES encryption algorithm.
   
2. Ransom Note Display:
- A graphical ransom note is displayed with an image and instructions to pay a ransom.
- A countdown timer creates urgency for the user to input the decryption key.**

3. File Decryption:
- If the correct key is provided, files are decrypted and restored to their original state.

## Ransomware Attack Simulation Workflow
- **Initial Infection**: The victim unknowingly acquires ransomware through email attachments or links.
- **Contacting the Attacker's C&C Server**: The ransomware connects to the attacker's command-and-control server to download the public key.
- **Data Encryption**: Files are encrypted using the public key, and a ransom note is displayed.
- **Ransom Payment and Decryption**: The victim must pay the ransom to receive the private key to decrypt the files.

## Prevention and Recommendations
To mitigate the risks posed by ransomware, follow these best practices:

- **Regular Backups**: Backup important data to offline or cloud storage.
- **Security Awareness**: Educate users on phishing and social engineering attacks.
- **Security Solutions**: Implement antivirus, firewalls, and intrusion detection systems.
- **Access Control**: Regularly review and update file permissions.

## Author
Sandarbh Kansal



