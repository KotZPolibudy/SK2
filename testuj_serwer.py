import socket
import sys
import ssl


def receive_message(socket):
    res = socket.recv()
    if b'\n' in res:
        res = res.split(b'\n', 1)[0]
    res = res.decode()
    if '\n' in res:
        res = res.split('\n', 1)[0]
    return res


def send_message(sock, message):
    sock.sendall(f"{message}\n".encode())


def check_winner(the_move):
    if the_move[-1] == "W":
        print("Wygrana!")
        return True
    elif the_move[-1] == "B":
        print("Przegrana, niestety")
        return True
    elif the_move[-1] == "D":
        print("Remis.")
        return True
    else:
        return False


def main(host, port):
    running = True
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1    # deprecated, ale chyba pomaga

    client_socket = socket.create_connection((host, port))
    ssl_socket = context.wrap_socket(client_socket, server_hostname=host)

    print("Oczekiwanie na przeciwnika... \n")

    color_message = receive_message(ssl_socket)
    print(color_message)
    if color_message[0] == 'W':
        my_color = 1
        print("Grasz jako białe!")
    else:
        my_color = 2
        print("Grasz jako czarne!")

    mylastmove = "Jeszcze nic!"
    lastmove = "Jeszcze tez nic!"
    mymove = "nico"
    server_res = "nie interere"

    while running:
        print("Moj ostatni ruch: ", mylastmove)
        print("Ostatni ruch przeciwnika; ", lastmove)

        if my_color == 1:
            mylastmove = mymove[:5]
            mymove = input()
            send_message(ssl_socket, mymove)
            if check_winner(mymove):
                break

            lastmove = server_res[:5]
            server_res = receive_message(ssl_socket)
            print(server_res)

        else:
            lastmove = server_res[:5]
            server_res = receive_message(ssl_socket)
            print(server_res)

            mylastmove = mymove[:5]
            mymove = input()
            send_message(ssl_socket, mymove)
            if check_winner(mymove):
                break

    # po grze:
    ssl_socket.close()  # rozłącz się
    wait = True
    while wait:
        a = input("Wpisz EXIT żeby wyjść")
        if a == "EXIT":
            break


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Podaj odpowiednie polecenie! \n python klient.py hostname port \n")
    else:
        ghost = sys.argv[1]
        gport = int(sys.argv[2])

        # gameplay loop
        main(ghost, gport)
