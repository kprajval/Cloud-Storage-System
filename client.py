import os
import socket
import ssl

SERVER_HOST = 'Praveena'
SERVER_PORT = 12345
BUFFER_SIZE = 4096
CERTFILE = 'projectCertificate.crt'
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')


def list_files(client_socket):
    client_socket.send("LIST_FILES".encode())
    files_list = client_socket.recv(BUFFER_SIZE).decode()
    print("\nAvailable files:")
    print(files_list)


def download_file(client_socket, filename, filesize):
    client_socket.send(f"DOWNLOAD|||{filename}".encode())
    file_data = client_socket.recv(BUFFER_SIZE).decode()

    if file_data.startswith("ERROR"):
        print(file_data)
    else:
        filepath = os.path.join(DOWNLOADS_FOLDER, filename)

        with open(filepath, 'wb') as f:
            total_received = 0
            while total_received < filesize:
                data = client_socket.recv(BUFFER_SIZE)
                total_received += len(data)
                f.write(data)

        print(f"[+] File downloaded to {filepath}")


def upload_file(client_socket, filename):
    try:
        with open(filename, 'rb') as f:
            file_data = f.read()
        client_socket.send(f"UPLOAD|||{filename}|||{file_data}".encode())
        response = client_socket.recv(BUFFER_SIZE).decode()
        print(response)  # Debug: Print response from the server
    except FileNotFoundError:
        print("Error: File not found.")
    except PermissionError:
        print("Error: Permission denied to open the file.")
    except Exception as e:
        print("Error:", e)


def delete_file(client_socket, filename):
    client_socket.send(f"DELETE|||{filename}".encode())
    print(client_socket.recv(BUFFER_SIZE).decode())


def main():
    client_ssl_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.load_verify_locations(CERTFILE)

        client_ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname=SERVER_HOST)
        client_ssl_socket.connect((SERVER_HOST, SERVER_PORT))

        while True:
            print("\n1. List files")
            print("2. Download file")
            print("3. Upload file")
            print("4. Delete file")
            print("5. Exit")
            choice = input("Enter your choice (1/2/3/4/5): ")

            if choice == '1':
                list_files(client_ssl_socket)

            elif choice == '2':
                filename = input("Enter filename to download: ")
                client_ssl_socket.send(f"DOWNLOAD|||{filename}".encode())
                response = client_ssl_socket.recv(BUFFER_SIZE).decode()
                if response.startswith("ERROR"):
                    print(response)
                else:
                    filename, filesize = response.split("|||")
                    filesize = int(filesize)
                    download_file(client_ssl_socket, filename, filesize)
                    print(f"[+] File {filename} downloaded successfully.")

            elif choice == '3':
                filename = input("Enter path of file to upload: ")
                if not os.path.exists(filename):
                    print("File not found.")
                else:
                    upload_file(client_ssl_socket, filename)

            elif choice == '4':
                filename = input("Enter filename to delete: ")
                delete_file(client_ssl_socket, filename)

            elif choice == '5':
                break

            else:
                print("Invalid choice. Please enter a valid option.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if client_ssl_socket:
            client_ssl_socket.close()


if __name__ == "__main__":
    main()
