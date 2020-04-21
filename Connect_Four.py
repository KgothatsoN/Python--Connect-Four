import pygame
import numpy as np
import sys
import math

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255,0, 0)
YELLOW = (255, 255, 0)
ROW = 6
COL = 7


def create_board():
    board = np.zeros((ROW, COL))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid(board, col):
    return board[ROW - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winner(board, piece):
    # Horizontal Win
    for c in range(COL - 3):
        for r in range(ROW):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Vertical
    for c in range(COL):
        for r in range(ROW - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Positive Diagonal
    for c in range(COL - 3):
        for r in range(ROW - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Negative Diagonal
    for c in range(COL - 3):
        for r in range(3, ROW):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


def draw_board(bord):
    for c in range(COL):
        for r in range(ROW):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COL):
        for r in range(ROW):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height-int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height-int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()
SQUARESIZE = 100
width = COL * SQUARESIZE
height = (ROW + 1) * SQUARESIZE
RADIUS = int(SQUARESIZE / 2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("serif", 90)

try:
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winner(board, 1):
                            label = myfont.render("Player 1 WINS!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                # Player 2 Input
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winner(board, 2):
                            label = myfont.render("Player 2 WINS!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True
                            break

                print_board(board)
                draw_board(board)
                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)

except ValueError:
    print("Invalid Input!")
