#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>

int PORT = 5001;

int main(void) {
    //connect to server
    struct sockaddr_in server_addr;
    int sock = socket(AF_INET,SOCK_STREAM,0);

    if (sock == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("Connection failed");
        close(sock);
        exit(EXIT_FAILURE);
    }

    //send and recieve
    char *message = "Hello Server!";
    char recieve_buffer[100];

    send(sock, message, strlen(message), 0);
    int bytes_recieved = recv(sock, recieve_buffer, 100, 0);
    recieve_buffer[bytes_recieved] = '\0';

    printf("Message from the server! %s\n", recieve_buffer);
    close(sock);
    return 0;
}