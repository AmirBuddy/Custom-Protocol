#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define SERVER_PORT 5000
#define CHUNK_SIZE 1024

int main() {
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len = sizeof(client_addr);
    int server_socket, bytes_received;
    char buffer[CHUNK_SIZE + 4];

    // Create UDP socket
    server_socket = socket(AF_INET, SOCK_DGRAM, 0);
    if (server_socket < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Initialize server address structure
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(SERVER_PORT);

    // Bind the socket to the server address
    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    printf("Server listening on %s:%d\n", "localhost", SERVER_PORT);

    while (1) {
        // Receive request from client
        bytes_received = recvfrom(server_socket, buffer, CHUNK_SIZE, 0, (struct sockaddr *)&client_addr, &client_addr_len);
        buffer[bytes_received] = '\0';
        if (strcmp(buffer, "request_permission") == 0) {
            // Send grant permission response
            sendto(server_socket, "granted", strlen("granted"), 0, (struct sockaddr *)&client_addr, client_addr_len);
            printf("Permission granted to client\n");

            // Receive file metadata
            bytes_received = recvfrom(server_socket, buffer, CHUNK_SIZE, 0, (struct sockaddr *)&client_addr, &client_addr_len);
            buffer[bytes_received] = '\0';
            char *token = strtok(buffer, ",");
            char *file_name = token;
            token = strtok(NULL, ",");
            char *file_format = token;
            token = strtok(NULL, ",");
            int file_size = atoi(token);
            printf("Receiving file: %s.%s (%d bytes)\n", file_name, file_format, file_size);

            // Send ready to receive file response
            sendto(server_socket, "ready", strlen("ready"), 0, (struct sockaddr *)&client_addr, client_addr_len);

            // Receive file chunks
            int chunks_received = 0;
            FILE *file = fopen(file_name, "wb");
            while (chunks_received < (file_size / CHUNK_SIZE) + 1) {
                bytes_received = recvfrom(server_socket, buffer, CHUNK_SIZE + 4, 0, (struct sockaddr *)&client_addr, &client_addr_len);
                int chunk_num;
                memcpy(&chunk_num, buffer, sizeof(int));
                fwrite(buffer + sizeof(int), 1, bytes_received - sizeof(int), file);
                printf("Received chunk %d\n", ntohl(chunk_num));

                // Send ACK
                sendto(server_socket, &chunk_num, sizeof(int), 0, (struct sockaddr *)&client_addr, client_addr_len);
                chunks_received++;
            }
            fclose(file);

            printf("File received and saved as %s\n", file_name);
        }
    }

    close(server_socket);
    return 0;
}
