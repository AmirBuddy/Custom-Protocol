import socket
import os

def read_file(file_path, chunk_size=1024):
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

def client(file_path):
    host = '127.0.0.1'
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    file_type = os.path.splitext(file_path)[1][1:]  # Extracting the file extension

    # Step 1: Send initial message
    client_socket.sendall(b"file_transfer_request")
    response = client_socket.recv(1024)  # Receive acknowledgment
    if response != b"ok":
        print("Server not ready for file transfer.")
        return

    # Step 2: Send file type and size
    file_size = os.path.getsize(file_path)
    file_info = f"{file_type},{file_size}"
    client_socket.sendall(file_info.encode('utf-8'))
    response = client_socket.recv(1024)  # Receive acknowledgment
    if response != b"ok":
        print("Server rejected file info.")
        return

    # Step 3: Send file data
    for chunk in read_file(file_path):
        client_socket.sendall(chunk)

    print("File sent successfully.")

    client_socket.close()

if __name__ == '__main__':
    file_path = input("Enter the path of the file: ")
    client(file_path)