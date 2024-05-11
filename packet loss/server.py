# server.py
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

    file_name = None
    file_size = 0
    bytes_received = 0
    packet_number = 0
    packet_buffer = {}

    while True:
        data, client_address = server_socket.recvfrom(1024)
        if data.startswith(b"file_transfer_request"):
            server_socket.sendto(b"ok", client_address)
            continue
        elif data.startswith(b"file_info,"):
            file_info = data.decode('utf-8').split(',')[1:]
            file_type, file_size = file_info
            file_size = int(file_size)
            file_name = f"uploaded_file.{file_type}"
            server_socket.sendto(b"ok", client_address)
            continue
        else:
            packet_number_received = int.from_bytes(data[:4], 'big')
            packet_data = data[4:]
            packet_buffer[packet_number_received] = packet_data
            server_socket.sendto(packet_number_received.to_bytes(4, 'big') + b"ok", client_address)
            while packet_number in packet_buffer:
                with open(file_name, 'ab') as f:
                    f.write(packet_buffer[packet_number])
                bytes_received += len(packet_buffer[packet_number])
                del packet_buffer[packet_number]
                packet_number += 1
                if bytes_received == file_size:
                    print(f"File received and saved as {file_name}")
                    return

if __name__ == '__main__':
    server()
