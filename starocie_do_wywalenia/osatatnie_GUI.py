import socket
import sys
import ssl
import os
import pygame

# Stałe:
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
BACKGROUND_COLOR = (188, 153, 105)
GRID_COLOR = (100, 100, 100)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (0, 255, 0, 100)


def receive_message(ssocket):
    try:
        res = ssocket.recv()
        if b'\n' in res:
            res = res.split(b'\n', 1)[0]
        res = res.decode()
        if '\n' in res:
            res = res.split('\n', 1)[0]
        return res
    except socket.error as er:
        print(f"Error receiving data: {er}")
        exit()


def send_message(sock, message):
    try:
        sock.sendall(f"{message}\n".encode())
    except socket.error as er:
        print(f"Error sending data: {er}")
        exit()


def placeholder_send(sock, message):
    print(f"Trust me bro, all sent!\n socket{sock}\n msg: {message}")


def placeholder_receive(ssocket):
    print(f"Trust me bro, all received from this socket{ssocket}\n")
    res = input()
    return res


def animation(info):
    global screen
    font = pygame.font.Font(None, 36)
    text = font.render(info, True, (128, 0, 128))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()


def handle_click(row, col):
    pass


def check_winner(board):
    count_white = board.count('w') + board.count('W')
    count_black = board.count('b') + board.count('B')
    if count_white == 0:
        return True, "B"
    elif count_black == 0:
        return True, "W"
    else:
        return False, "None"


def handle_win(winner):
    pass


def get_possible_moves(board):
    pass


def draw_board(board, possible_moves, current_player, player):
    screen.fill(BACKGROUND_COLOR)

    # Draw grid
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
        pygame.draw.line(screen, GRID_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))

    # Draw pieces and possible moves
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = col * CELL_SIZE, row * CELL_SIZE
            if (current_player == player):
                if (row, col) in possible_moves:
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(screen, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 2)  # Outline

            if board[row][col] == 'b':
                pygame.draw.circle(screen, BLACK_COLOR, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            elif board[row][col] == 'w':
                pygame.draw.circle(screen, WHITE_COLOR, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            elif board[row][col] == 'B':
                pygame.draw.circle(screen, WHITE_COLOR, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            elif board[row][col] == 'W':
                pygame.draw.circle(screen, WHITE_COLOR, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

    pygame.display.flip()


def main(server_address, server_port, color):
    board = "Pbbbbbbbbbbbb........wwwwwwwwwwww"
    made_move = False
    current_player = "W"
    selected_square = "None"
    possible_moves = get_possible_moves(board)

    # Rysuj plansze
    draw_board(board, possible_moves, current_player, color)

    # pętla gry:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif current_player == color and not made_move:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    handle_click(col, row)

        # Rysuj plansze
        possible_moves = get_possible_moves(board)
        draw_board(board, possible_moves, current_player, color)
        # Koniec?
        is_there_winner, who = check_winner(board)
        if is_there_winner:
            handle_win(who)
            pygame.quit()
            exit()
        # ticknij zegar gry - koniec pętli gry
        pygame.time.Clock().tick(60)


# Tutaj START
# Inicjalizacja pygame
pygame.init()

# Inicjacja okienka
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Warcaby")

if len(sys.argv) != 3:
    print("Podaj odpowiednie polecenie! \n python klient.py hostname port \n")
else:
    host = sys.argv[1]
    port = int(sys.argv[2])

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # deprecated, ale chyba pomaga
    client_socket = socket.create_connection((host, port))
    ssl_socket = context.wrap_socket(client_socket, server_hostname=host)

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

    # i tutaj main!
    main(host, port, my_color)
