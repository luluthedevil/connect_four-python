import numpy as np
import pygame
import sys
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
YELLOW = (200, 200, 0)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, column, piece):
    board[row][column] = piece


def is_valid_location(board, column):
    return board[ROW_COUNT-1][column] == 0


def get_next_open_row(board, column):
    for r in range(ROW_COUNT):
        if board[r][column] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # cheking horizontals for win
    for col in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True

    # cheking verticals for win
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True

    # cheking positively diaganols for win
    for col in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT - 3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True

    # cheking negative diaganols for win
    for col in range(COLUMN_COUNT - 3):
        for row in range(3, ROW_COUNT):
            if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True


def draw_board(board):
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (col*SQUARE_SIZE, row*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

            pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0
pygame.init()

SQUARE_SIZE = 100
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE
size = (width, height)

RADIUS = int(SQUARE_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

my_font = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            # Ask player 1 input
            if turn == 0:
                posx = event.pos[0]
                column = int(math.floor(posx / SQUARE_SIZE))
                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 1)

                    if winning_move(board, 1):
                        label = my_font.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (30, 10))
                        game_over = True

            # Ask player 2 input
            else:
                posx = event.pos[0]
                column = int(math.floor(posx / SQUARE_SIZE))
                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 2)

                    if winning_move(board, 2):
                        label = my_font.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (30, 10))
                        game_over = True

            print_board(board)
            draw_board(board)
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)