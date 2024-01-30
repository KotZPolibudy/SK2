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


def print_curr_board():
    global board
    i = 0
    for double_row in range(4):
        print(f" . {board[i]} . {board[i+1]} . {board[i+2]} . {board[i+3]} \n {board[i+4]} . {board[i+5]} . {board[i+6]} . {board[i+7]}")
        i += 8


def makeboard(old_board, start, finish):
    s = old_board[start]
    new_board = ""
    if start < finish:
        new_board = old_board[:start] + "." + old_board[start + 1:finish] + s + old_board[finish + 1:]
        # new_board = old_board[:start]
        # new_board += "."
        # new_board += old_board[start+1 : finish]
        # new_board += s
        # new_board += old_board[finish+1 :]
    else:
        new_board = old_board[:finish] + s + old_board[finish + 1:start] + "." + old_board[start + 1:]
        # new_board = old_board[:finish]
        # new_board += s
        # new_board += old_board[finish + 1: start]
        # new_board += "."
        # new_board += old_board[start + 1:]
    return new_board


def make_move_from_input(move_a, move_b):
    global board
    a = "U"
    a += move_a
    a += move_b
    a += makeboard(board, move_a, move_b)
    return a


def make_the_move(MOVE):
    global board
    move_start = MOVE[1:3]   # wytnij pole z ruchu i przerob na int
    move_fin = MOVE[3:5]
    board = makeboard(board, int(move_start), int(move_fin))


def make_the_move2(raw_move):
    global board
    i = 0
    while raw_move[i] == 'U':
        move_start = raw_move[i+1:i+3]
        move_fin = raw_move[i+3:i+5]
        # board = makejump  skoki kurcze


def main(host, port):
    global board
    global legal_moves
    global legal_captures
    board = "bbbbbbbbbbbb........wwwwwwwwwwww"

    running = True
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # deprecated, ale chyba pomaga

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
            make_the_move(mymove)
            send_message(ssl_socket, mymove)
            if check_winner(mymove):
                break

            lastmove = server_res[:5]
            server_res = receive_message(ssl_socket)
            print(server_res)
            make_the_move(server_res)

        else:
            lastmove = server_res[:5]
            server_res = receive_message(ssl_socket)
            print(server_res)
            make_the_move(server_res)

            mylastmove = mymove[:5]
            mymove = input()
            make_the_move()
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

    """
    . b . b . b . b
    b . b . b . b .
    . b . b . b . b
    . . . . . . . .
    . . . . . . . . 
    w . w . w . w .
    . w . w . w . w 
    w . w . w . w .


    .. 01 .. 02 .. 03 .. 04
    05 .. 06 .. 07 .. 08 ..
    .. 09 .. 10 .. 11 .. 12
    13 .. 14 .. 15 .. 16 ..
    .. 17 .. 18 .. 19 .. 20
    21 .. 22 .. 23 .. 24 ..
    .. 25 .. 26 .. 27 .. 28
    29 .. 30 .. 31 .. 32 ..
    """


board = "bbbbbbbbbbbb........wwwwwwwwwwww"
legal_moves = [[1, 5], [1, 6], [2, 6], [2, 7], [3, 7], [3, 8], [4, 8],
               [5, 9], [6, 9], [6, 10], [7, 10], [7, 11], [8, 11], [8, 12],
               [9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16],
               [13, 17], [14, 17], [14, 18], [15, 18], [15, 19], [16, 19], [16, 20],
               [17, 21], [17, 22], [18, 22], [18, 23], [19, 23], [19, 24], [20, 24],
               [21, 25], [22, 25], [22, 26], [23, 26], [23, 27], [24, 27], [24, 28],
               [25, 29], [25, 30], [26, 30], [26, 31], [27, 31], [27, 32], [28, 32]]

legal_captures = [[1, 10], [2, 9], [2, 11], [3, 10], [3, 12], [4, 11],
                  [5, 14], [6, 13], [6, 15], [7, 14], [7, 16], [8, 15],
                  [9, 18], [10, 17], [10, 19], [11, 18], [11, 20], [12, 19],
                  [13, 22], [14, 21], [14, 23], [15, 22], [15, 24], [16, 23],
                  [17, 26], [18, 25], [18, 27], [19, 26], [19, 28], [20, 27],
                  [21, 30], [22, 29], [22, 31], [23, 30], [23, 32], [24, 31]]

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Podaj odpowiednie polecenie! \n python klient.py hostname port \n")
    else:
        ghost = sys.argv[1]
        gport = int(sys.argv[2])

        # gameplay loop
        main(ghost, gport)
