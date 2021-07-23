// Cliente de aplicação TCP/IP usando socket C/Linux
// Autor: Leticia Sales 
// Professor: Elias P. Duarte Jr
// Data: 22/julho/2021

#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> // DNS: Domain Name System
#include <stdlib.h>
#include <string.h>

int main(int argc, char const *argv[])
{
  int sock_descr;
  int rec_bytes_num;
  struct sockaddr_in remote_addr;
  struct hostent *dns_register;
  char buffer[BUFSIZ];
  const char *hostname;
  const char *dados;

  if (argc != 4) {
    puts("Uso correto: cliente <nome servidor> <porta servidor> <dados>");
    return -1;
  }

  hostname = argv[1];
  dados = argv[3];

  if ((dns_register = gethostbyname(hostname)) == NULL) {
    puts("Erro ao obter o endereço do servidor");
    return -1;
  }

  // Se chegou aqui, conseguiu!

  bcopy((char*)dns_register->h_addr, (char*)&remote_addr.sin_addr, dns_register->h_length);

  remote_addr.sin_family = AF_INET;
  remote_addr.sin_family = htons(atoi(argv[2])); // converts from little engine to big engine

  if ((sock_descr = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
    puts("Erro ao abrir o socket");
    return -1;
  }

  if (connect(sock_descr, (struct sockaddr *) &remote_addr, sizeof(remote_addr)) < 0) {
    puts("Erro ao conectar ao servidor");
    return -1;
  }

  // Se chegou aqui, tá conectado!

  if (write(sock_descr, dados, strlen(dados)) != strlen(dados)) {
    puts("Erro ao transmitir os dados");
    return -1;
  }

  read(sock_descr, buffer, BUFSIZ); // bloqueante

  printf("Sou o cliente, recebi %s\n", buffer);

  return 0;
}