import socket
import struct

# Server settings
SERVER_HOST = 'localhost'
SERVER_PORT = 5000
CHUNK_SIZE = 1024

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))

print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

while True:
    # Receive request from client
    data, address = server_socket.recvfrom(1024)
    if data.decode() == 'request_permission':
        # Send grant permission response
        server_socket.sendto(b'granted', address)
        print("Permission granted to client")

        # Receive file metadata
        data, address = server_socket.recvfrom(1024)
        file_name, file_format, file_size = data.decode().split(',')
        file_size = int(file_size)
        print(f"Receiving file: {file_name}.{file_format} ({file_size} bytes)")

        # Send ready to receive file response
        server_socket.sendto(b'ready', address)

        # Receive file chunks
        chunks_received = {}
        while len(chunks_received) < (file_size // CHUNK_SIZE) + 1:
            data, address = server_socket.recvfrom(CHUNK_SIZE + 4)
            chunk_num = struct.unpack('!I', data[:4])[0]
            chunk_data = data[4:]
            chunks_received[chunk_num] = chunk_data
            print(f"Received chunk {chunk_num}")

            # Send ACK
            server_socket.sendto(struct.pack('!I', chunk_num), address)

        # Reassemble file
        with open(f'new-{file_name}', 'wb') as f:
            for i in range((file_size // CHUNK_SIZE) + 1):
                f.write(chunks_received[i])

        print(f"File received and saved as {file_name}")