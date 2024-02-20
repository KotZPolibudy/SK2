import socket
import sys
import ssl
import tkinter as tk
from PIL import Image, ImageTk
import os

last_clicked = None
first_click = None
is_first_click = True
image_dir = "klient/images"


def refresh_board(canvas, board_string):
    global ssl_socket
    board_string = board_string[1:]
    for i in range(len(board_string)):
        row = i // 4
        if row % 2 == 0:
            col = (i % 4) * 2 + 1
        else:
            col = (i % 4) * 2
        pawn_type = board_string[i]
        draw_pawn(canvas, row, col, pawn_type)


def draw_board(canvas):
    canvas.pawn_images = []
    for row in range(8):
        for col in range(8):
            color = "darkgreen" if (row + col) % 2 == 1 else "white"
            square_id = canvas.create_rectangle(col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color)
            if color == "darkgreen":
                canvas.tag_bind(square_id, "<Button-1>", lambda event, square_id=square_id: on_click(event, square_id))
            else:
                canvas.tag_bind(square_id, "<Button-1>", lambda event: reset_clicked())


def draw_pawn(canvas, row, col, pawn_type):
    if pawn_type == ".":
        return  # No image, just blank button

    color = "white" if pawn_type.lower() == "w" else "black"
    is_king = pawn_type.isupper()
    pawn_name = "king" if is_king else "pawn"
    filename = os.path.join(image_dir, f"{color}-{pawn_name}.png")

    image = Image.open(filename)
    image = image.resize((40, 40))
    pawn_image = ImageTk.PhotoImage(image)
    pawn_button = tk.Button(canvas, image=pawn_image, borderwidth=0, highlightthickness=0,
                            command=lambda row=row, col=col: on_pawn_click(row, col))
    pawn_button.image = pawn_image  # Keep a reference to prevent garbage collection
    canvas.create_window((col * 50 + 25, row * 50 + 25), window=pawn_button)
    canvas.pawn_buttons.append(pawn_button)


def on_click(event, square_id):
    global last_clicked, first_click, is_first_click
    global canvas, board
    col = event.x // 50
    row = event.y // 50
    if (row + col) % 2 == 1:  # Dark green square
        square_number = get_square_number(row, col)
        if is_first_click:
            first_click = square_number
            is_first_click = False
        else:
            # print("Clicked functional:", first_click, square_number)
            move_from_input(first_click, square_number)  # Call move_from_input function with clicked squares
            refresh_board(canvas, board)
            enemy_turn = True
            is_first_click = True
        if last_clicked:
            canvas.itemconfig(last_clicked, outline='')  # Clear previous highlighting
        canvas.itemconfig(square_id, outline='red')  # Highlight current dark green square
        last_clicked = square_id
    else:
        reset_clicked()
        # print("Clicked white")


def on_pawn_click(row, col):
    global last_clicked, first_click, is_first_click
    field_number = get_square_number(row, col)
    # print("Pawn clicked at field number:", field_number)
    reset_clicked()
    first_click = field_number
    is_first_click = False
    canvas.itemconfig(field_number, outline='red')
    last_clicked = field_number



def reset_clicked():
    global last_clicked, first_click, is_first_click
    if last_clicked:
        canvas.itemconfig(last_clicked, outline='')  # Clear previous highlighting
        last_clicked = None
        first_click = None
        is_first_click = True


def get_square_number(row, col):
    if row % 2 == 0:
        return (row * 4) + (col // 2) + 1
    else:
        return ((row - 1) * 4) + ((col - 1) // 2) + 6


def move_from_input(start, finish):
    global board
    global legal_moves
    global legal_captures
    global ssl_socket
    err = True
    print(f"Move from {start} to {finish}")

    s = int(start)
    f = int(finish)
    start = str(s)
    finish = str(f)
    if board[s] != "." and board[f] == ".":
        if [s, f] in legal_moves or [f, s] in legal_moves:
            a = "U" + start + finish
            # return a
            board = makeboard(board, s, f)
            err = False

        elif [s, f] in legal_captures:
            for x in range(5, 29):
                if [s, x] in legal_moves and [x, f] in legal_moves and board[x] != ".":
                    a = "U" + start + finish
                    # return a
                    board = makeboard(board, s, f)
                    err = False
        elif [f, s] in legal_captures:
            for x in range(5, 29):
                if [f, x] in legal_moves and [x, s] in legal_moves and board[x] != ".":
                    a = "U" + start + finish
                    # return a
                    board = makeboard(board, s, f)
                    err = False

    if err:
        print("Podaj prawidlowy ruch!")

def handleturn(start, finish, a):
    global board
    global ssl_socket
    board = makeboard(board, start, finish)
    send_message(ssl_socket, a)
    server_res = receive_message(ssl_socket)
    move=make_the_move(server_res)


def receive_message(ssocket):
    res = ssocket.recv()
    if b'\n' in res:
        res = res.split(b'\n', 1)[0]
    res = res.decode()
    if '\n' in res:
        res = res.split('\n', 1)[0]
    return res


def send_message(sock, message):
    sock.sendall(f"{message}\n".encode())


def send_message_globalsock(message):
    global ssl_socket
    ssl_socket.sendall(f"{message}\n".encode())



def print_board_scheme():
    print(".. 01 .. 02 .. 03 .. 04 \n"
          "05 .. 06 .. 07 .. 08 .. \n"
          ".. 09 .. 10 .. 11 .. 12 \n"
          "13 .. 14 .. 15 .. 16 .. \n"
          ".. 17 .. 18 .. 19 .. 20 \n"
          "21 .. 22 .. 23 .. 24 .. \n"
          ".. 25 .. 26 .. 27 .. 28 \n"
          "29 .. 30 .. 31 .. 32 .. \n\n")


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
    i = 1
    print("Current boardstate: ")
    for double_row in range(4):
        print(f" . {board[i]} . {board[i+1]} . {board[i+2]} . {board[i+3]} \n {board[i+4]} . {board[i+5]} . {board[i+6]} . {board[i+7]} .")
        i += 8


def makeboard(old_board, start, finish):
    s = old_board[start]
    if start < finish:
        new_board = old_board[:start] + "." + old_board[start + 1:finish] + s + old_board[finish + 1:]
    else:
        new_board = old_board[:finish] + s + old_board[finish + 1:start] + "." + old_board[start + 1:]
    # jeszcze if bicie to usuniecie bitego
    if abs(start-finish) > 6:
        old_board = new_board
        if finish < start:
            start, finish = finish, start
        for x in range(5, 29):
            if [start, x] in legal_moves and [x, finish] in legal_moves:
                new_board = old_board[:x] + "." + old_board[x+1:]
    return new_board


def make_move_from_input_text():
    global board
    global legal_moves
    global legal_captures
    while True:
        start = input("Podaj skąd się ruszasz: ")
        finish = input("Podaj dokąd się ruszasz: ")
        s = int(start)
        f = int(finish)
        if board[s] != "." and board[f] == ".":
            if [s, f] in legal_moves or [f, s] in legal_moves:
                a = "U" + start + finish
                return a
            elif [s, f] in legal_captures:
                for x in range(5, 29):
                    if [s, x] in legal_moves and [x, f] in legal_moves and board[x] != ".":
                        a = "U" + start + finish
                        return a
            elif [f, s] in legal_captures:
                for x in range(5, 29):
                    if [f, x] in legal_moves and [x, s] in legal_moves and board[x] != ".":
                        a = "U" + start + finish
                        return a

        print("Podaj prawidlowy ruch!")


def make_the_move(MOVE):
    global board
    move_start = MOVE[1:3]   # wytnij pole z ruchu i przerob na int
    move_fin = MOVE[3:5]
    board = makeboard(board, int(move_start), int(move_fin))
    # print_curr_board()


def make_the_jump(raw_move):
    global board
    i = 0
    while raw_move[i] == 'U':
        move_start = raw_move[i+1:i+3]
        move_fin = raw_move[i+3:i+5]
        i += 5
        # board = makejump  skoki kurcze


def main(host, port):
    global board
    global legal_moves
    global legal_captures
    board = "Pbbbbbbbbbbbbeeeeeeeewwwwwwwwwwww"  # pierwszy znak nie ma znaczenia, oznacza Planszę

    global canvas

    running = True

    # Połączenie z przeciwnikiem
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

    # tutaj rzeczy z GUI, włączenie "gry" po znalezieniu przeciwnika
    root = tk.Tk()
    root.title("Wracaby")
    canvas = tk.Canvas(root, width=400, height=400, bg="white")
    canvas.pack()
    canvas.pawn_images = []
    canvas.pawn_buttons = []
    draw_board(canvas)
    refresh_board(canvas, board)
    root.mainloop()

    # stare - do przeprowadzenia gry tekstowo - ale działa, a GUI powoduje problemy :(
    while running:
        print_curr_board()
        print("Moj ostatni ruch: ", mylastmove)
        print("Ostatni ruch przeciwnika; ", lastmove)

        if my_color == 1:
            # mymove = input()
            mymove = make_move_from_input_text()
            make_the_move(mymove)
            send_message(ssl_socket, mymove)
            print_curr_board()
            if check_winner(mymove):
                break

            server_res = receive_message(ssl_socket)
            print(server_res)
            make_the_move(server_res)

        else:
            server_res = receive_message(ssl_socket)
            print(server_res)
            make_the_move(server_res)

            # mymove = input()
            mymove = make_move_from_input_text()
            make_the_move(mymove)
            send_message(ssl_socket, mymove)
            if check_winner(mymove):
                break
        mylastmove = mymove[:5]
        lastmove = server_res[:5]

    # po grze:
    ssl_socket.close()  # rozłącz się
    wait = True
    while wait:
        a = input("Wpisz EXIT żeby wyjść")
        if a == "EXIT":
            break

    """
    pomocniczy schemat planszy:
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

global ssl_socket

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Podaj odpowiednie polecenie! \n python klient.py hostname port \n")
    else:
        ghost = sys.argv[1]
        gport = int(sys.argv[2])

        # gameplay loop
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # deprecated, ale chyba pomaga
        client_socket = socket.create_connection((ghost, gport))
        ssl_socket = context.wrap_socket(client_socket, server_hostname=ghost)
        main(ghost, gport)
