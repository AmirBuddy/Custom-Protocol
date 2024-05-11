import socket
import os

def save_file(file_name, file_data):
    with open(file_name, 'wb') as f:
        f.write(file_data)

def server():
    host = '127.0.0.1'
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Server is listening...")

    connection, client_address = server_socket.accept()
    print(f"Connected by {client_address}")

    initial_message = connection.recv(1024)  # Receive initial message
    print("received initial message")
    if initial_message == b"file_transfer_request":  # Check if it's a file transfer request
        connection.sendall(b"ok")  # Send acknowledgment
        file_info = connection.recv(1024)  # Receive file info
        file_type, file_size = file_info.decode('utf-8').split(',')
        file_size = int(file_size)
        connection.sendall(b"ok")  # Send acknowledgment
        file_name = f"uploaded_file.{file_type}"
        with open(file_name, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_size:
                chunk = connection.recv(1024)
                f.write(chunk)
                bytes_received += len(chunk)
        print(f"File received and saved as {file_name}")

    connection.close()

if __name__ == '__main__':
    server()