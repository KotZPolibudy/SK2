import socket
import sys
import ssl
import pygame
from draughts import Board, Move, WHITE, BLACK
import tkinter as tk
from tkinter import PhotoImage


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
    

def get_square(pos, my_color):
    pass


def draw_highlights(board, square, my_color):
    pass


def new_board(board, my_color):
    pass

def promotion(board, my_color, selected_square, target_square):
    pass


def _move(selected_square, target_square, my_color):
    pass


def loading(info):
    global screen
    font = pygame.font.Font(None, 36)
    text = font.render(info, True, (128, 0, 128))
    text_rect = text.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def move_from_txt():
    global board
    pom = board.legal_moves()
    print("Legalne ruchy: ")
    print(pom)
    print("Którym pionkiem?  ")
    a = input()
    print("Na jakie pole?  ")
    b = input()
    return [a, b]


def move_from_gui():
    return move_from_txt()


def move_from_opponent(opponent_move):
    global screen
    global board
    global my_color
    rec = opponent_move



def check_winner(the_move):
    if the_move[0] == "W":
        loading("Wygrana!")
        return True
    elif the_move[0] == "B":
        loading("Przegrana, niestety")
        return True
    elif the_move[0] == "D":
        loading("Remis.")
        return True
    else:
        return False


def main(host, port):
    global screen
    global board 
    global my_color
    global turn
    running = True

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    client_socket = socket.create_connection((host, port))
    ssl_socket = context.wrap_socket(client_socket, server_hostname=host)
    loading("Oczekiwanie na godnego przeciwnika")

    color_message = receive_message(ssl_socket)
    if color_message == 'W':
        my_color = 1
    else:
        my_color = 2

    # start the game
    board = Board(variant="standard", fen="startpos")

    while running:
        print(board)
        if my_color == 1:
            mymove = move_from_gui()
            send_message(ssl_socket, mymove)
            if check_winner(mymove):
                break

            server_res = receive_message(ssl_socket)
            move_from_opponent(server_res)
            if check_winner(server_res):
                break

        else:
            server_res = receive_message(ssl_socket)
            move_from_opponent(server_res)
            if check_winner(server_res):
                break

            mymove = move_from_gui()
            send_message(ssl_socket, mymove)
            if check_winner(mymove):
                break

    # po grze:
    ssl_socket.close()  # rozłącz się
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                wait = False
    pygame.quit()   # Wyjdz wtedy jak uzytkownik powie wyjdz.


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Podaj odpowiednie polecenie! \n python klient.py hostname port \n")
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        
        pygame.init()
        
        #  Ustawienia ekranu
        WIN_WIDTH = 640
        WIN_HEIGHT = 640
        window_size = (WIN_WIDTH, WIN_HEIGHT)
        screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Checkers")
        
        # gameplay loop
        main(host, port)
        