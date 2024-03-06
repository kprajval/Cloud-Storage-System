import os
import socket
import ssl
from threading import Thread

SERVER_PORT = 12345
BUFFER_SIZE = 4096
BASE_DIRECTORY = 'path of your cloud storage directory'
CERTFILE = 'projectCertificate.crt'
KEYFILE = 'projectKey.key'


def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE).decode()

            if not data:
                break

            if data.startswith("LIST_FILES"):
                files_list = os.listdir(BASE_DIRECTORY)
                if files_list:
                    files_str = "\n".join(files_list)
                    client_socket.send(files_str.encode())
                else:
                    client_socket.send("Empty folder".encode())

            elif data.startswith("DOWNLOAD|||"):
                filename = data.split("|||")[1]
                filepath = os.path.join(BASE_DIRECTORY, filename)
                if os.path.exists(filepath):
                    filesize = os.path.getsize(filepath)
                    client_socket.send(f"{filename}|||{filesize}".encode())
                    with open(filepath, 'rb') as f:
                        while True:
                            data = f.read(BUFFER_SIZE)
                            if not data:
                                break
                            client_socket.sendall(data)
                    print("[+] File downloaded successfully.")
                else:
                    client_socket.send("ERROR: File not found.".encode())

            elif data.startswith("UPLOAD"):
                filename, file_data = data.split("|||")[1], data.split("|||")[2]
                filepath = os.path.join(BASE_DIRECTORY, filename)

                with open(filepath, 'wb') as f:
                    f.write(file_data.encode())
                client_socket.send("File uploaded successfully.".encode())

            elif data.startswith("DELETE"):
                filename = data.split("|||")[1]
                filepath = os.path.join(BASE_DIRECTORY, filename)

                if os.path.exists(filepath):
                    os.remove(filepath)
                    client_socket.send("File deleted successfully.".encode())
                else:
                    client_socket.send("ERROR: File not found.".encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def main():
    if not os.path.exists(BASE_DIRECTORY):
        os.makedirs(BASE_DIRECTORY)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('server_ip_address', SERVER_PORT))
    server_socket.listen(5)

    print(f"[*] Listening on port {SERVER_PORT}")

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
            client_ssl_socket = ssl_context.wrap_socket(client_socket, server_side=True)
            client_thread = Thread(target=handle_client, args=(client_ssl_socket,))
            client_thread.start()

    except KeyboardInterrupt:
        print("\n[*] Server shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
