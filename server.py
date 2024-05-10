import socket
import os

def save_file(file_name, file_data):
    with open(file_name, 'wb') as f:
        f.write(file_data)

def server():
    host = '127.0.0.1'
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print("Server is listening...")

    while True:
        initial_message, client_address = server_socket.recvfrom(1024)  # Receive initial message
        if initial_message == b"file_transfer_request":  # Check if it's a file transfer request
            server_socket.sendto(b"ok", client_address)  # Send acknowledgment
            file_info, _ = server_socket.recvfrom(1024)  # Receive file info
            file_type, file_size = file_info.decode('utf-8').split(',')
            file_size = int(file_size)
            server_socket.sendto(b"ok", client_address)  # Send acknowledgment
            file_data, _ = server_socket.recvfrom(file_size + 1024)  # Receive file data
            file_name = f"uploaded_file.{file_type}"
            save_file(file_name, file_data)
            print(f"File received and saved as {file_name}")
            break  # Break after receiving file data once

if __name__ == '__main__':
    server()