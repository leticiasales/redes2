// Servidor de aplicação TCP/IP usando socket C/Linux
// Recebe string do cliente e retorna o mesmo ao cliente
// Autor: Leticia Sales 
// Professor: Elias P. Duarte Jr
// Data: 22/julho/2021

#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdlib.h>
#include <string.h>

#define TAMFILA 5
#define MAXHOSTNAME 30

int main(int argc, char const *argv[])
{
  int sock_listen, sock_answer;
  unsigned int aux;
  char buffer[BUFSIZ];
  struct sockaddr_in local_addr, remote_addr;
  struct hostent *dns_register;
  char hostname[MAXHOSTNAME];

  // signal();

  if (argc != 2) {
    puts ("Uso correto: servidor <porta>");
    return -1;
  }

  gethostname(hostname, MAXHOSTNAME);

  if ((dns_register = gethostbyname(hostname)) == NULL) {
    puts("Erro ao obter IP");
    return -1;
  }

  local_addr.sin_port = htons(atoi(argv[1]));
  local_addr.sin_family = AF_INET;
  bcopy((char*) dns_register->h_addr, (char*) &remote_addr.sin_addr, dns_register->h_length);

  if ((sock_listen = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
    puts("Erro ao abrir o socket.");
    return -1;
  }
  
  if (bind(sock_listen, (struct sockaddr *) &local_addr, sizeof(local_addr)) < 0){
    puts ("Erro ao fazer o bind");
    return -1;
  }    

  listen(sock_listen, TAMFILA);

  while (1) {
    aux = sizeof(remote_addr);

    if ((sock_answer = accept(sock_listen, (struct sockaddr*) &remote_addr, &aux)) < 0) {
      puts("Erro ao aceitar conexão");
      return -1;
    }

    read(sock_answer, buffer, BUFSIZ);
    printf("Sou o servidor, recebi a mensagem %s\n", buffer);
    write(sock_answer, buffer, BUFSIZ);
    close(sock_answer);
  }

 return 0;
}