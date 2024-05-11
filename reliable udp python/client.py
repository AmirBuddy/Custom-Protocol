import socket
import struct
import os

# Client settings
SERVER_HOST = 'localhost'
SERVER_PORT = 5000
CHUNK_SIZE = 1024

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ask user for file path
file_path = input("Enter the file path: ")

if os.path.isfile(file_path):
    file_name = os.path.basename(file_path)
    file_format = os.path.splitext(file_path)[1][1:]
    file_size = os.path.getsize(file_path)

    # Send request to server
    client_socket.sendto(b'request_permission', (SERVER_HOST, SERVER_PORT))
    print("Requesting permission from server")

    # Receive grant permission response
    data, address = client_socket.recvfrom(1024)
    if data.decode() == 'granted':
        print("Permission granted by server")

        # Send file metadata
        client_socket.sendto(f"{file_name},{file_format},{file_size}".encode(), (SERVER_HOST, SERVER_PORT))

        # Receive ready to receive file response
        data, address = client_socket.recvfrom(1024)
        if data.decode() == 'ready':
            print("Server is ready to receive file")

            # Send file chunks
            with open(file_path, 'rb') as f:
                chunk_num = 0
                while True:
                    chunk_data = f.read(CHUNK_SIZE)
                    if not chunk_data:
                        break
                    client_socket.sendto(struct.pack('!I', chunk_num) + chunk_data, (SERVER_HOST, SERVER_PORT))
                    chunk_num += 1
                    print(f"Sent chunk {chunk_num}")

                    # Receive ACK
                    data, address = client_socket.recvfrom(4)
                    ack_chunk_num = struct.unpack('!I', data)[0]
                    print(f"Received ACK for chunk {ack_chunk_num}")

    print("File sent successfully")
else:
    print("File not found")