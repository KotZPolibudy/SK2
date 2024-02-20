// gcc mojserwer.C -o mojserver -lssl -lcrypto <- aby skomplilować
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/wait.h>
#include <sys/select.h>
#include <bits/pthreadtypes.h>
#include <openssl/ssl.h>
#include <openssl/crypto.h>

#define MAX_MESSAGE_LENGTH 66
/*
0: Stan gry    // g - gramy w - wygrana
1-64: stan pól
65: \n
*/

int _write(SSL* ssl, char *buf, int len)
{
	while (len > 0) {
	    int i = SSL_write(ssl, buf, len);
	    len -= i;
	    buf += i;
	}
    return 0;
}

int _read(SSL* ssl, char *buf, int bufsize)
{
	int totalRead = 0;
	do
	{
		int i = SSL_read(ssl, buf + totalRead, bufsize);
		bufsize -= i;
		totalRead += i;
	} while (buf[totalRead - 1] != '\n' && bufsize > 0);
	if(buf[totalRead - 1] == '\n') totalRead--;
    return totalRead;
}

struct cln
{
	int cfd;
	struct sockaddr_in caddr;
};

struct player{
    char message[MAX_MESSAGE_LENGTH];
    int opponent_fd;
    SSL* ssl;
    bool color;
};

struct player* players;


    pthread_mutex_t mut_count;  // Ilość graczy w sekcji krytycznej
    pthread_mutex_t mut_waiting; // Tylko jeden gracz czeka
    pthread_mutex_t mut_dlugo_jeszcze; // Anty aktywne czekanie

    int player_count = 0, waiting_fd = -1;  // do parowania
    char buf[256];
    SSL_CTX* ctx;

int game_init(int size)
{
    players = (struct player*)calloc(size+1, sizeof(struct player));
    if (players == NULL) {
        printf("NULL PLAYERS ERR\n");
        exit(0);
    } else {
        printf("Game innit.\n");
        return 1;
    }
}

int update_count_players(int size)
{
    struct player* temp = players;
    players = (struct player*)realloc(players, size * sizeof(struct player));
    if (!players) {
        players = temp;
        return -1;
    } else {
        return 1;
    }
}

void* cthread(void* arg) {
    struct cln *c = (struct cln *) arg;
    printf("[%lu] new connection from: %s:%d\n",
           (unsigned long int) pthread_self(),
           inet_ntoa((struct in_addr) c->caddr.sin_addr),
           ntohs(c->caddr.sin_port)
    );
    printf("%d\n", c->cfd);

    // SSL setup for this thread
    players[c->cfd].ssl = SSL_new(ctx);
    if (!players[c->cfd].ssl) {
        printf("SSL creation error.\n");
        free(c);
        return NULL;
    }
    SSL_set_fd(players[c->cfd].ssl, c->cfd);

    // SSL Handshake
    if (SSL_accept(players[c->cfd].ssl) <= 0) {
        printf("SSL handshake error.\n");
        SSL_free(players[c->cfd].ssl);
        free(c);
        return NULL;
    }
   pthread_mutex_lock(&mut_waiting);
    if(waiting_fd == -1)
    {
        waiting_fd = c->cfd;
        pthread_mutex_unlock(&mut_waiting);
        pthread_mutex_lock(&mut_dlugo_jeszcze);
    }
    else //jeśli ktoś czeka
    {
        players[c->cfd].opponent_fd = waiting_fd;
        players[waiting_fd].opponent_fd = c->cfd;
        players[c->cfd].color = 1;
        players[waiting_fd].color = 0;
        players[c->cfd].message[0] = 'U';
        players[waiting_fd].message[0] = 'U';
        waiting_fd = -1;
        //To uwalnia czekającego
        pthread_mutex_unlock(&mut_dlugo_jeszcze);
        pthread_mutex_unlock(&mut_waiting);
    }
    printf("Let's play: %d, %d \n", c->cfd, players[c->cfd].opponent_fd);
    if(players[c->cfd].color == 0)
    {
        //Ty masz czerwone...
        _write(players[c->cfd].ssl, "W\n", 2);
    }
    else
    {
        //A ty czarne...
        _write(players[c->cfd].ssl, "B\n", 2);
    }
    if(players[c->cfd].color == 0)
    {

        /*
        Gracze przesyłają sobie ruchy a serwer ich *nie weryfikuje*

        Nie jest to najlepsze podejście jeśli idzie o możliwości naruszania fair-play, ale jednocześnie ułatwi
        to ogromnie implementacje serwera, który i tak jest już dość skomplikowany 'as is'.
        */
        while(1)
        {
            // Czytaj pierwszego, wyślij drugiemu.
            _read(players[c->cfd].ssl, players[c->cfd].message, sizeof(players[c->cfd].message));
            _write(players[players[c->cfd].opponent_fd].ssl, players[c->cfd].message, sizeof(players[c->cfd].message));
            //Koniec?
            if(players[c->cfd].message[0] != 'U')
            {
                break;
            }
            //Czytaj drugiego, wyślij pierwszemu
            _read(players[players[c->cfd].opponent_fd].ssl, players[players[c->cfd].opponent_fd].message, sizeof(players[players[c->cfd].opponent_fd].message));
            _write(players[c->cfd].ssl, players[players[c->cfd].opponent_fd].message, sizeof(players[players[c->cfd].opponent_fd].message));
            //Koniec?
            if(players[players[c->cfd].opponent_fd].message[0] != 'U')
            {
                break;
            }
        }
        close(players[c->cfd].opponent_fd);
        close(c->cfd);
    }
    
    free(c);
    pthread_mutex_lock(&mut_count);
    player_count--;
    pthread_mutex_unlock(&mut_count);
	return 0;
}


int main(int argc, char** argv)
{
    pthread_t tid;
    int sfd, on = 1;
    sfd = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
    setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, (char*)&on, sizeof(on));
    socklen_t sl;
    struct sockaddr_in saddr, caddr;
    memset(&saddr, 0, sizeof(saddr));
    saddr.sin_family = AF_INET;
    saddr.sin_addr.s_addr = INADDR_ANY;
    saddr.sin_port = htons(1234);
    bind(sfd, (struct sockaddr*)&saddr, sizeof(saddr));
    listen(sfd, 10);

    SSL_library_init();
    SSL_load_error_strings();
    ctx = SSL_CTX_new(TLS_server_method());
    if (!ctx) {
        printf("SSL context creation error.\n");
        return EXIT_FAILURE;
    }
    // Ścieżki do certyfikatu i klucza prywatnego serwera dla SSL
    if (SSL_CTX_use_certificate_file(ctx, "server.crt", SSL_FILETYPE_PEM) <= 0 ||
        SSL_CTX_use_PrivateKey_file(ctx, "server.key", SSL_FILETYPE_PEM) <= 0) {
        printf("Certificate or key loading error.\n");
        SSL_CTX_free(ctx);
        return EXIT_FAILURE;
    }

    game_init(2);

    // żeby grać musi mieć przeciwnika
    pthread_mutex_lock(&mut_dlugo_jeszcze);
    // while - game loop
    while (1) {
        struct cln* c = (cln*)malloc(sizeof(struct cln));
        sl = sizeof(c->caddr);
        c->cfd = accept(sfd, (struct sockaddr*)&c->caddr, &sl);
        if (c->cfd != -1) {
            pthread_mutex_lock(&mut_count); // licz ile graczy - sekcja krytyczna
            player_count++;
            // parowanie przeciwników (upewnić się że jest dokładnie dwóch, załadować do (zmiennych żeby znali siebie nawzajem?)
            if (update_count_players(c->cfd + 1) == -1) {
                write(c->cfd, "E\n", 2); //Error - zbyt wielu graczy
                pthread_mutex_unlock(&mut_count);
                continue; // ale samotnego gracza przypadkiem nie wysyłaj do gry
            }
            pthread_mutex_unlock(&mut_count); //wyjście z krytycznej - odblokuj wszystko
            pthread_create(&tid, NULL, cthread, c);
            // i pthread_detach żeby tamta parka poszła sobie grać -> cthread ma implementacje przekazywania sobie wiadomości.
            pthread_detach(tid);
        }
    }

    SSL_CTX_free(ctx);
    close(sfd);
    return 0;
}