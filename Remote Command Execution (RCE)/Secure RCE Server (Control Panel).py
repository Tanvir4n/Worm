import socket
import ssl

# Configuration for SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')

def start_server():
    server_ip = '0.0.0.0'
    server_port = 12345

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_sock = context.wrap_socket(sock, server_side=True)

    secure_sock.bind((server_ip, server_port))
    secure_sock.listen(5)

    print("[*] Listening for incoming connections...")

    try:
        client_socket, client_address = secure_sock.accept()
        print(f"[*] Connection from {client_address}")

        while True:
            # Send command to the client
            command = input("Enter command: ")

            if command.lower() == 'exit':
                client_socket.send(b'exit')
                break
            else:
                client_socket.send(command.encode())
                response = client_socket.recv(4096).decode()
                print(response)

    finally:
        client_socket.close()
        secure_sock.close()

if __name__ == "__main__":
    start_server()
