import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BROWN = (188, 153, 105)
GREEN = (0, 255, 0)
CROWN = (235, 255, 52)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

# Board
board = [[0, 1, 0, 1, 0, 1, 0, 1],
         [2, 0, 1, 0, 1, 0, 1, 0],
         [0, 1, 0, 1, 0, 1, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, -1, 0, -1, 0, -1, 0],
         [0, -1, 0, -1, 0, -1, 0, -1],
         [-1, 0, -1, 0, -1, 0, -1, 0]]

# Functions
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] > 0:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 30)
                if board[row][col] == 2:
                    pygame.draw.circle(screen, CROWN, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 20)
            elif board[row][col] < 0:
                pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 30)
                if board[row][col] == -2:
                    pygame.draw.circle(screen, CROWN, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 20)


def draw_highlights(possible_moves):
    for move in possible_moves:
        row, col = move
        pygame.draw.rect(screen, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

def highlights_possible_moves(moves,selected_piece):
    for move in moves:
        if(move == selected_piece):
            continue
        row, col = move
        pygame.draw.rect(screen, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)


def get_pice_can_take(row,col,turn):
    takes=[]
    directions = [(1, 1), (1, -1),(-1, 1), (-1, -1)]
    for d_row,d_col in directions:
        new_row,new_col=row+d_row,col+d_col
        if 0 <= new_row+d_row < ROWS and 0 <= new_col+d_col < COLS and ((board[new_row][new_col] < 0) if turn > 0 else (board[new_row][new_col] > 0)) and board[new_row+d_row][new_col+d_col] == 0:
            #print(board[row][col])
            takes.append((row,col))
            break
    return takes

def get_pice_takes(row,col,turn):
    takes=[]
    directions = [(1, 1), (1, -1),(-1, 1), (-1, -1)]
    for d_row, d_col in directions:
        new_row, new_col = row + d_row, col + d_col
        if 0 <= new_row < ROWS and 0 <= new_col < COLS and ((board[new_row][new_col] < 0) if turn > 0 else (board[new_row][new_col] > 0)):
            jump_row, jump_col = new_row + d_row, new_col + d_col
            if 0 <= jump_row < ROWS and 0 <= jump_col < COLS and board[jump_row][jump_col] == 0:
                takes.append((jump_row, jump_col))
    #print(takes)
    return takes

def get_queen_takes(row,col,turn):

    takes=[]
    #if(board[row][col])
    directions = [(1, 1), (1, -1),(-1, 1), (-1, -1)]
    for d_row, d_col in directions:
        new_row, new_col = row + d_row, col + d_col
        while 0 <= new_row < ROWS and 0 <= new_col < COLS and board[new_row][new_col] == 0:
            new_row, new_col = new_row + d_row, new_col + d_col
        if 0 <= new_row < ROWS and 0 <= new_col < COLS and ((board[new_row][new_col] < 0) if turn > 0 else (board[new_row][new_col] > 0)):
            jump_row, jump_col = new_row + d_row, new_col + d_col
            if 0 <= jump_row < ROWS and 0 <= jump_col < COLS and board[jump_row][jump_col] == 0:
                takes.append((jump_row, jump_col))
    return takes

    takes=[]
    directions = [(1, 1), (1, -1),(-1, 1), (-1, -1)]
    for d_row, d_col in directions:
        new_row, new_col = row + d_row, col + d_col
        if 0 <= new_row < ROWS and 0 <= new_col < COLS and ((board[new_row][new_col] < 0) if turn > 0 else (board[new_row][new_col] > 0)):
            jump_row, jump_col = new_row + d_row, new_col + d_col
            if 0 <= jump_row < ROWS and 0 <= jump_col < COLS and board[jump_row][jump_col] == 0:
                takes.append((jump_row, jump_col))
    print(takes)
    return takes

def get_pice_moves(row,col):
    moves=[]
    directions = [(1, 1), (1, -1)] if board[row][col] == 1 else [(-1, 1), (-1, -1)]
    for d_row, d_col in directions:
        new_row, new_col = row + d_row, col + d_col
        if 0 <= new_row < ROWS and 0 <= new_col < COLS and board[new_row][new_col] == 0:
            moves.append((new_row, new_col))
    return moves

def get_queen_moves(row,col):
    moves=[]
    #if(board[row][col])
    directions = [(1, 1), (1, -1),(-1, 1), (-1, -1)]
    for d_row, d_col in directions:
        new_row, new_col = row + d_row, col + d_col
        while 0 <= new_row < ROWS and 0 <= new_col < COLS and board[new_row][new_col] == 0:
            moves.append((new_row, new_col))
            new_row, new_col = new_row + d_row, new_col + d_col
    return moves

def get_takes(turn):
    takes=[]
    if turn > 0:
        for row in range(ROWS):
            for col in range(COLS):
                if not(board[row][col]>0):
                    continue
                if board[row][col]==1:
                    takes += get_pice_can_take(row,col,turn)
                elif len(get_queen_takes(row,col,turn)):
                    takes.append((row,col))
    else:
        for row in range(ROWS):
            for col in range(COLS):
                if not(board[row][col]<0):
                    continue
                if board[row][col]==-1:
                    takes += get_pice_can_take(row,col,turn)
                elif len(get_queen_takes(row,col,turn)):
                    takes.append((row,col))
    return takes
            

def get_moving(turn):
    moves=[]
    directions = [(1, 1), (1, -1),(-1, 1), (-1, -1)]
    for row in range(ROWS):
        for col in range(COLS):
            if not((board[row][col] < 0) if turn < 0 else (board[row][col] > 0)):
                continue
            if(abs(board[row][col] == 1)):
                directions = [(1, 1), (1, -1)] if board[row][col] == 1 else [(-1, 1), (-1, -1)]
                for d_row, d_col in directions:
                    new_row, new_col = row + d_row, col + d_col
                    if 0 <= new_row < ROWS and 0 <= new_col < COLS and board[new_row][new_col] == 0:
                        moves.append((row,col))
                        break
            else:
                if len(get_queen_moves(row,col)) > 0:
                    moves.append((row,col))
    return moves
            

def get_possible_moves(selected_piece,turn,takes):
    possible_moves = []
    row, col = selected_piece
    if takes:
        if abs(board[row][col]) == 1:
            possible_moves = get_pice_takes(row,col,turn)
        elif abs(board[row][col]) == 2:
            possible_moves+=get_queen_takes(row,col,turn)
    else:
        if abs(board[row][col]) == 1:
            possible_moves+=get_pice_moves(row,col)
        elif abs(board[row][col]) == 2:
            possible_moves+=get_queen_moves(row,col)
    return possible_moves



def main():
    turn = 1  # 1 for Red, -1 for Black
    selected_piece = None
    running = True
    started_move = False
    idonno=0
    while running:
        #screen.fill(WHITE)
        draw_board()
        draw_pieces()

        takes=get_takes(turn)
        
        if selected_piece is not None:
            possible_moves=get_possible_moves(selected_piece,turn,len(takes)>0)
            draw_highlights(possible_moves)
        if not started_move:
            if(len(takes)>0):
                highlights_possible_moves(takes,selected_piece)
            else:
                moves=get_moving(turn)
                highlights_possible_moves(moves,selected_piece)

        if(idonno>=60):
            #if len(takes)>0:
                #print("PossTakes")
                #print(takes)
            idonno=0
        idonno+=1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // SQUARE_SIZE
                row = event.pos[1] // SQUARE_SIZE
                #if board[row][col] == turn and not started_move:
                if ((board[row][col] < 0) if turn < 0 else (board[row][col] > 0) ) and not started_move:
                    selected_piece = (row, col)
                elif selected_piece is not None and (row, col) in possible_moves:
                    board[row][col] = board[selected_piece[0]][selected_piece[1]]
                    board[selected_piece[0]][selected_piece[1]] = 0
                    # Remove captured piece if there's a jump
                    if abs(row - selected_piece[0]) >= 2:
                        #captured_row = (row + selected_piece[0]) // 2
                        #captured_col = (col + selected_piece[1]) // 2
                        captured_row = row - 1
                        captured_col = col - 1
                        if(row < selected_piece[0]):
                            captured_row = row + 1
                        if(col < selected_piece[1]):
                            captured_col = col + 1
                        board[captured_row][captured_col] = 0
                        # Check for additional captures
                        selected_piece = (row, col)
                        if(selected_piece in get_takes(turn)):
                            started_move=True
                            continue
                        started_move=False
                    if turn > 0:
                        if row == ROWS - 1:
                            if board[row][col]==1:
                                board[row][col]=2
                    else:
                        if row == 0:
                            if board[row][col]==-1:
                                board[row][col]=-2

                    selected_piece = None
                    turn *= -1



        pygame.display.update()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
