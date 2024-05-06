#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>

// struct in_addr {
//     unsigned long s_addr;
// };

// struct sockaddr_in {
//     short sin_family;
//     unsigned short sin_port;
//     struct in_addr sin_addr;
//     char sin_zero;
// };

int main(void) {
    //set up server
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in server_addr;
    char storage_buffer[80];

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(5001);

    int binder = bind(sock, (struct sockaddr *) &server_addr, sizeof(server_addr));
    if (binder == -1){
        perror("Binding failed");
        close(sock);
        exit(EXIT_FAILURE);
    }

    if (listen(sock, 3) == -1) {
        perror("listen");
        close(sock);
        EXIT_FAILURE;
    }
    printf("Server is Live!");

    //connect to client
    int client;
    struct sockaddr_in client_addr;
    socklen_t client_len = sizeof(client_addr);

    int client_sock = accept(sock, (struct sockaddr *)&client_addr, &client_len);
    if (client_sock < 0) {
        perror("Couldn't establish connection with client");
        exit(EXIT_FAILURE);
    }

    //recieve and send
    char *message = "Hello Client";
    send(client_sock, message, strlen(message), 0);
    char buffer[1024];
    int bytes_recieved = recv(client_sock, buffer, sizeof(buffer), 0);
    buffer[bytes_recieved] = '\0';
    printf("Recived: %s\n", buffer);

    close(client_sock);
    close(sock);
    return 0;
}