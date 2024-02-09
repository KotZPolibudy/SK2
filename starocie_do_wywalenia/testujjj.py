import socket
import sys
import ssl


def receive_message(client_socket):
    res = b""
    while True:
        chunk = client_socket.recv(256)
        if not chunk:
            break
        res += chunk
        if b'\n' in res:
            res = res.split(b'\n', 1)[0]
            break
        return res.decode()


def send_message(sock, message):
    sock.sendall(f"{message}\n".encode())


def check_winner(the_move):
    if the_move[0] == "W":
        print("Wygrana!")
        return True
    elif the_move[0] == "B":
        print("Przegrana, niestety")
        return True
    elif the_move[0] == "D":
        print("Remis.")
        return True
    else:
        return False


def main(host, port):
    running = True
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    client_socket = socket.create_connection((host, port))
    ssl_socket = context.wrap_socket(client_socket, server_hostname=host)

    print("Oczekiwanie na przeciwnika... \n")

    color_message = receive_message(ssl_socket)
    print(color_message)
    if color_message == 'W':
        my_color = 1
        print("Grasz jako białe!")
    else:
        my_color = 2
        print("Grasz jako czarne!")

    mylastmove = "Jeszcze nic!"
    lastmove = "Jeszcze tez nic!"
    mymove = "nico"
    server_res ="nie interere"

    while running:
        print(mylastmove)
        print(lastmove)

        if my_color == 1:
            mylastmove = mymove
            mymove = input()
            send_message(ssl_socket, mymove)
            if check_winner(mymove):
                break

            lastmove = server_res
            server_res = receive_message(ssl_socket)
            print(server_res)

        else:
            lastmove = server_res
            server_res = receive_message(ssl_socket)
            print(server_res)

            mylastmove = mymove
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