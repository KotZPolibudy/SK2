import socket
import sys
import ssl
import tkinter as tk


class CheckersGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Checkers")

        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="white")
        self.canvas.pack()

        self.last_clicked = None  # Store the ID of the last clicked black square
        self.first_click = None  # Store the ID of the first clicked black square
        self.is_first_click = True  # Flag to indicate whether it's the first click in the sequence

        self.draw_board()

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = "darkgreen" if (row + col) % 2 == 1 else "white"
                square_id = self.canvas.create_rectangle(col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color)
                if color == "darkgreen":
                    self.canvas.tag_bind(square_id, "<Button-1>", lambda event, square_id=square_id: self.on_click(event, square_id))
                else:
                    self.canvas.tag_bind(square_id, "<Button-1>", lambda event: self.reset_clicked())

    def on_click(self, event, square_id):
        col = event.x // 50
        row = event.y // 50
        if (row + col) % 2 == 1:  # Dark green square
            square_number = self.get_square_number(row, col)
            if self.is_first_click:
                self.first_click = square_number
                self.is_first_click = False
            else:
                print("Clicked functional:", self.first_click, square_number)
                self.is_first_click = True
            if self.last_clicked:
                self.canvas.itemconfig(self.last_clicked, outline='')  # Clear previous highlighting
            self.canvas.itemconfig(square_id, outline='red')  # Highlight current dark green square
            self.last_clicked = square_id
        else:
            self.reset_clicked()
            print("Clicked white")

    def reset_clicked(self):
        if self.last_clicked:
            self.canvas.itemconfig(self.last_clicked, outline='')  # Clear previous highlighting
            self.last_clicked = None
            self.first_click = None
            self.is_first_click = True

    def get_square_number(self, row, col):
        if row % 2 == 0:
            return (row * 4) + (col // 2) + 1
        else:
            return ((row - 1) * 4) + ((col - 1) // 2) + 6


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
        for x in range(5,29):
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
    print_curr_board()


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
    board = "Pbbbbbbbbbbbb........wwwwwwwwwwww"  # pierwszy znak nie ma znaczenia, oznacza Planszę

    root = tk.Tk()
    gui = CheckersGUI(root)
    root.mainloop()

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
        print_curr_board()
        print("Moj ostatni ruch: ", mylastmove)
        print("Ostatni ruch przeciwnika; ", lastmove)

        if my_color == 1:
            # mymove = input()
            mymove = make_move_from_input_text()
            make_the_move(mymove)
            send_message(ssl_socket, mymove)
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

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Podaj odpowiednie polecenie! \n python klient.py hostname port \n")
    else:
        ghost = sys.argv[1]
        gport = int(sys.argv[2])

        # gameplay loop
        main(ghost, gport)

