import pygame
import sys
import socket
import ssl

from Board import Board
from Game import Game

pygame.init()

class Checkers:
	def __init__(self, screen):
		self.screen = screen
		self.running = True
		self.FPS = pygame.time.Clock()

	def _draw(self, board):
		board.draw(self.screen)
		pygame.display.update()

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

	def main(self, window_width, window_height, host, port):

		context = ssl.create_default_context()
		context.check_hostname = False
		context.verify_mode = ssl.CERT_NONE

		context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # deprecated, ale chyba pomaga

		client_socket = socket.create_connection((host, port))
		ssl_socket = context.wrap_socket(client_socket, server_hostname=host)

		print("Oczekiwanie na przeciwnika... \n")

		color_message = receive_message(ssl_socket)
		print("Grasz jako: ", color_message)
		if color_message[0] == 'W':
			my_color = 1
			print("Grasz jako białe!")
		else:
			my_color = 2
			print("Grasz jako czarne!")

		board_size = 8
		tile_width, tile_height = window_width // board_size, window_height // board_size
		board = Board(tile_width, tile_height, board_size, socket)
		game = Game()
		while self.running:
			game.check_jump(board)

			for self.event in pygame.event.get():
				if self.event.type == pygame.QUIT:
					self.running = False

				if not game.is_game_over(board):
					if self.event.type == pygame.MOUSEBUTTONDOWN:
						board.handle_click(self.event.pos)
				else:
					game.message()
					self.running = False

			self._draw(board)
			self.FPS.tick(60)


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Podaj odpowiednie polecenie! \n python klient.py hostname port \n")
	else:
		ghost = sys.argv[1]
		gport = int(sys.argv[2])

		# start gameplay loop
		window_size = (640, 640)
		screen = pygame.display.set_mode(window_size)
		pygame.display.set_caption("Checkers")

		checkers = Checkers(screen)
		checkers.main(window_size[0], window_size[1], ghost, gport)

