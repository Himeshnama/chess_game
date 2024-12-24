import pygame
import sys
import copy
from Move_functions import *
from stockfish import Stockfish
import chess
import math
from image_diff import *
from camera import *
import cv2

####################### SETTINGS ########################### 


pygame.init()
pygame.display.set_caption("Chess With Achachan")

WIDTH = 578
HEIGHT = 578

BLACK = (0, 0, 0)
RED = (225, 0, 0)
GREEN = (0, 225, 0)
BLUE = (0, 0, 255)
GREY = (107, 107, 107)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (33, 39, 49)
TOP_COLOUR = (240, 240, 240)
GOLDEN = (218, 165, 32)

FPS = 27


####################### APP CLASS ###########################


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.chess_board = pygame.image.load("Chess Board.jpg")
        self.B_King = pygame.image.load("B - King.png")
        self.B_Minister = pygame.image.load("B - Minister.png")
        self.B_Rook = pygame.image.load("B - Rook.png")
        self.B_Bishop = pygame.image.load("B - Bishop.png")
        self.B_Horse = pygame.image.load("B - Horse.png")
        self.B_Pawn = pygame.image.load("B - Pawn.png")
        self.W_King = pygame.image.load("W - King.png")
        self.W_Minister = pygame.image.load("W - Minister.png")
        self.W_Rook = pygame.image.load("W - Rook.png")
        self.W_Bishop = pygame.image.load("W - Bishop.png")
        self.W_Horse = pygame.image.load("W - Horse.png")
        self.W_Pawn = pygame.image.load("W - Pawn.png")
        self.dot = pygame.image.load("Dot.png")
        self.Checkmate_image = pygame.image.load("Checkmate.png")
        self.border_space = 25
        self.mouse_pos = pygame.mouse.get_pos()
        self.box_pos = self.pix_to_square(self.mouse_pos[0], self.mouse_pos[1])
        self.clicked_board_pos = ()
        self.clicked = False
        self.selected_piece = None
        self.piece_type = None
        self.selected_piece_colour = None
        self.movable_pos = []
        self.selected_piece_pos = ()
        self.whose_turn = "White"
        self.checkmate = False
        self.outcome = None
        self.moves_till_now = []
        self.stockfish = Stockfish()
        self.board = chess.Board()
        self.pressed = False
        capture_img("img1.png")
        #self.stockfish.set_elo_rating(100)
        self.B_Pos = {
            "Black King": (5, 8),
            "Black Minister": (4, 8),
            "Black Bishop": {"Black B1": (3, 8), "Black B2": (6, 8)},
            "Black Horse": {"Black H1": (2, 8), "Black H2": (7, 8)},
            "Black Rook": {"Black R1": (1, 8), "Black R2": (8, 8)},
            "Black Pawn": {"Black P1": (1, 7), "Black P2": (2, 7), "Black P3": (3, 7), "Black P4": (4, 7),
                           "Black P5": (5, 7), "Black P6": (6, 7), "Black P7": (7, 7), "Black P8": (8, 7)}
        }
        self.W_Pos = {
            "White King": (5, 1),
            "White Minister": (4, 1),
            "White Bishop": {"White B1": (3, 1), "White B2": (6, 1)},
            "White Horse": {"White H1": (2, 1), "White H2": (7, 1)},
            "White Rook": {"White R1": (1, 1), "White R2": (8, 1)},
            "White Pawn": {"White P1": (1, 2), "White P2": (2, 2), "White P3": (3, 2), "White P4": (4, 2),
                           "White P5": (5, 2), "White P6": (6, 2), "White P7": (7, 2),
                           "White P8": (8, 2)}
        }
        self.B_movable_poses = None
        self.W_movable_poses = None
        self.in_check = False
        self.pins = []
        self.checks = []
        self.move_functions = Move_Functions(self)

    def run(self):
        while self.running and self.outcome is None:
            self.events()
            self.updates()
            self.draw()
            self.clock.tick(FPS)
        print(len(self.moves_till_now))
        if self.outcome is not None:
            if self.outcome[0] == "Checkmate":
                if self.outcome[1] == "Winner = White":
                    time = 0
                    while self.running and time < 1000:
                        time += 1
                        self.events()
                        self.screen.fill(BLACK)
                        self.screen.blit(self.chess_board, (0, 0))
                        self.draw_players()
                        self.screen.blit(self.Checkmate_image, (120, 180))
                        pygame.display.update()
                else:
                    print("White won")
            else:
                print("It is a draw")
            pygame.quit()
        sys.exit()

    def events(self):
        self.clicked = False
        self.pressed = False
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                self.running = False

            if events.type == pygame.MOUSEBUTTONUP:
                self.clicked = True

            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_SPACE:
                    self.pressed = True

        self.mouse_pos = pygame.mouse.get_pos()

    def updates(self):
        if self.whose_turn == "White":
            if self.pressed:
                print('clicking picture and saving as img2.png')
                capture_img("img2.png")
                pos1, pos2 = get_move("img1.png", "img2.png", self.board)
                pos1, pos2 = self.correct_move(pos1, pos2, False)
                print(pos1, pos2)
                letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]

                move = str(letters[pos1[0] - 1]) + str(pos1[1]) + str(letters[pos2[0] - 1]) + str(pos2[1])
                move = chess.Move.from_uci(move)
                if move not in self.board.legal_moves:
                    print("ILLEGAL MOVE!")
                    self.running = False
                    self.run()
                self.fluid_move(pos1, pos2)
                self.record_move(pos1, pos2)
                self.whose_turn = "Black"
                self.outcome = self.get_outcome()

        else:
            if self.whose_turn == "Black":
                self.screen.fill(BLACK)
                self.screen.blit(self.chess_board, (0, 0))
                self.draw_players()
                pygame.display.update()
                self.play_best_move()
                self.outcome = self.get_outcome()
                self.whose_turn = "Black -- Waiting"
            elif self.whose_turn == "Black -- Waiting":
                if self.pressed:
                    print("clicking picture and storing as img1.png")
                    capture_img("img1.png")
                    print("MAKE MOVE")
                    self.whose_turn = "White"

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.chess_board, (0, 0))
        self.draw_players()

        pygame.display.update()

    ####################### HELP FUNCTIONS ###########################

    def play_best_move(self):
        best_move = self.FindBestMove(self.moves_till_now)
        if len(best_move) == 4:
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]
            selected_piece_pos = (letters.index(best_move[0]) + 1, int(best_move[1]))
            pos = (letters.index(best_move[2]) + 1, int(best_move[3]))
            self.fluid_move(selected_piece_pos, pos)
            self.record_move(selected_piece_pos, pos)
        else:
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]
            selected_piece_pos = (letters.index(best_move[0]) + 1, int(best_move[1]))
            pos = (letters.index(best_move[2]) + 1, int(best_move[3]))
            self.fluid_move(selected_piece_pos, pos)
            self.moves_till_now.append(best_move)
            move_on_board = chess.Move.from_uci(best_move)
            self.board.push(move_on_board)

    def convert_square(self, move):
        col = ['8', '7', '6', '5', '4', '3', '2', '1']
        square = (int(col[move[0]-1]) , move[1])
        return square

    def correct_move(self, start_pos, end_pos, from_diff):
        if not from_diff:
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]
            move = str(letters[start_pos[0] - 1]) + str(start_pos[1]) + str(letters[end_pos[0] - 1]) + str(end_pos[1])
            move = chess.Move.from_uci(move)
            if move in self.board.legal_moves:
                return start_pos, end_pos
            else:
                return end_pos, start_pos
        else:
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]
            move = str(letters[start_pos[0] - 1]) + str(start_pos[1]) + str(letters[end_pos[0] - 1]) + str(end_pos[1])
            move = chess.Move.from_uci(move)
            if move in self.board.legal_moves:
                return start_pos, end_pos
            else:
                start_pos, end_pos = end_pos, start_pos
                move = str(letters[start_pos[0] - 1]) + str(start_pos[1]) + str(letters[end_pos[0] - 1]) + str(end_pos[1])
                move = chess.Move.from_uci(move)
                if move in self.board.legal_moves:
                    return start_pos, end_pos
        return None, None
        

    def draw_grid(self, width, height, cell_width, cell_height, border_space):
        for x in range(9):
            pygame.draw.line(self.screen, RED, ((x * cell_width) + border_space, border_space),
                             ((x * cell_width) + border_space, height + border_space))
        for x in range(9):
            pygame.draw.line(self.screen, RED, (border_space, (x * cell_height) + border_space),
                             (width + border_space, (x * cell_height) + border_space))

    def square_to_pix(self, x, y, border_space):
        modified_y = 8 - (y - 1)
        pix_x = ((x - 1) * 66) + border_space
        pix_y = ((modified_y - 1) * 66) + (border_space + 1)
        coordinates = (pix_x, pix_y)

        return coordinates

    def pix_to_square(self, pix_x, pix_y):
        x = 1 + int((pix_x - 27) / 66)
        if x > 8:
            x = 8
        elif x < 1:
            x = 1

        y = 1 + int((pix_y - 27) / 66)
        y = 8 - (y - 1)
        if y > 8:
            y = 8
        elif y < 1:
            y = 1

        coordinates = (x, y)
        return coordinates

    def draw_players(self):
        pieces = {'k': self.B_King,
                  'q': self.B_Minister,
                  'r': self.B_Rook,
                  'b': self.B_Bishop,
                  'n': self.B_Horse,
                  'p': self.B_Pawn,
                  'K': self.W_King,
                  'Q': self.W_Minister,
                  'R': self.W_Rook,
                  'B': self.W_Bishop,
                  'N': self.W_Horse,
                  'P': self.W_Pawn,
                  }
        for i in range(0, 64):
            piece = str(self.board.piece_at(i))
            if piece != "None":
                if (i + 1) % 8 != 0:
                    x = (i + 1) % 8
                    y = ((i + 1) // 8) + 1
                else:
                    x = 8
                    y = (i + 1) // 8
                pos = self.square_to_pix(x, y, self.border_space)
                self.screen.blit(pieces[piece], pos)

    def draw_box(self, position, selected):
        if selected:
            pix_pos = self.square_to_pix(position[0], position[1], self.border_space)
            pygame.draw.rect(self.screen, GREEN, (pix_pos[0], pix_pos[1], 65, 65), 3)
        else:
            pix_pos = self.square_to_pix(position[0], position[1], self.border_space)
            pygame.draw.rect(self.screen, GOLDEN, (pix_pos[0], pix_pos[1], 65, 65), 3)

    def identify_piece(self):
        piece = None
        for x in self.W_Pos:
            if x == "White Rook" or x == "White Bishop" or x == "White Horse" or x == "White Pawn":
                for i in self.W_Pos[x]:
                    if self.W_Pos[x][i] == self.clicked_board_pos:
                        piece = i
                        self.selected_piece_colour = "White"
                        if x == "White Rook":
                            self.piece_type = "Rook"
                        elif x == "White Bishop":
                            self.piece_type = "Bishop"
                        elif x == "White Horse":
                            self.piece_type = "Horse"
                        else:
                            self.piece_type = "Pawn"

            else:
                if self.clicked_board_pos == self.W_Pos[x]:
                    piece = x
                    self.selected_piece_colour = "White"
                    if x == "White King":
                        self.piece_type = "King"
                    else:
                        self.piece_type = "Minister"

        for x in self.B_Pos:
            if x == "Black Rook" or x == "Black Bishop" or x == "Black Horse" or x == "Black Pawn":
                for i in self.B_Pos[x]:
                    if self.B_Pos[x][i] == self.clicked_board_pos:
                        piece = i
                        self.selected_piece_colour = "Black"
                        if x == "Black Rook":
                            self.piece_type = "Rook"
                        elif x == "Black Bishop":
                            self.piece_type = "Bishop"
                        elif x == "Black Horse":
                            self.piece_type = "Horse"
                        else:
                            self.piece_type = "Pawn"

            else:
                if self.clicked_board_pos == self.B_Pos[x]:
                    piece = x
                    self.selected_piece_colour = "Black"
                    if x == "Black King":
                        self.piece_type = "King"
                    else:
                        self.piece_type = "Minister"

        return piece

    def get_all_valid_movable_poses(self, B_Pos, W_Pos, colour):
        '''legal_moves = self.board.legal_moves()
        if colour == "Black":
            for move in legal_moves:
                pass
        '''
        self.pins, self.checks, self.in_check = self.find_pins_and_checks(B_Pos, W_Pos, colour)
        if colour == "Black":
            king_pos = self.get_pos_for_piece("Black", "Black King", B_Pos, W_Pos)
            king_row = king_pos[0]
            king_col = king_pos[1]
            if self.in_check:
                if len(self.checks) == 1:
                    B_movable_poses = self.move_functions.get_all_B_movable_poses(B_Pos, W_Pos, self.pins)
                    check = self.checks[0]
                    check_row = check[0]
                    check_col = check[1]
                    piece_checking = self.get_piece_for_pos(B_Pos, W_Pos, (check_row, check_col))
                    valid_squares = []
                    if "Horse" in piece_checking:
                        valid_squares = [(check_row, check_col)]
                    else:
                        for i in range(1, 8):
                            valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                            valid_squares.append(valid_square)
                            if valid_square[0] == check_row and valid_square[1] == check_col:
                                break

                    for movable_piece in B_movable_poses:
                        B_movable_poses_copy = copy.deepcopy(B_movable_poses)
                        for move in B_movable_poses_copy[movable_piece]:
                            if "King" not in movable_piece:
                                if not (move[0], move[1]) in valid_squares:
                                    B_movable_poses[movable_piece].remove(move)
                else:
                    B_movable_poses = {
                        "Black King": self.move_functions.get_B_King_movable_pos((king_row, king_col), B_Pos, W_Pos),
                        "Black Pawn": {}
                    }
            else:
                B_movable_poses = self.move_functions.get_all_B_movable_poses(B_Pos, W_Pos, self.pins)

            return B_movable_poses
        else:
            king_pos = self.get_pos_for_piece("White", "White King", B_Pos, W_Pos)
            king_row = king_pos[0]
            king_col = king_pos[1]
            if self.in_check:
                if len(self.checks) == 1:
                    W_movable_poses = self.move_functions.get_all_W_movable_poses(B_Pos, W_Pos, self.pins)
                    check = self.checks[0]
                    check_row = check[0]
                    check_col = check[1]
                    piece_checking = self.get_piece_for_pos(B_Pos, W_Pos, (check_row, check_col))
                    valid_squares = []
                    if "Horse" in piece_checking:
                        valid_squares = [(check_row, check_col)]
                    else:
                        for i in range(1, 8):
                            valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                            valid_squares.append(valid_square)
                            if valid_square[0] == check_row and valid_square[1] == check_col:
                                break
                    for movable_piece in W_movable_poses:
                        W_movable_poses_copy = copy.deepcopy(W_movable_poses)
                        for move in W_movable_poses_copy[movable_piece]:
                            if "King" not in movable_piece:
                                if not (move[0], move[1]) in valid_squares:
                                    W_movable_poses[movable_piece].remove(move)
                else:
                    W_movable_poses = {
                        "White King": self.move_functions.get_W_King_movable_pos((king_row, king_col), B_Pos, W_Pos),
                        "White Pawn": {}
                    }
            else:
                W_movable_poses = self.move_functions.get_all_W_movable_poses(B_Pos, W_Pos, self.pins)

            return W_movable_poses

    def get_all_B_movable_poses(self, B_Pos, W_Pos):
        B_movable_poses = {}
        for piece_t in B_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in B_Pos[piece_t]:
                    if "R" in piece:
                        B_movable_poses[piece] = (
                            self.move_functions.get_B_Rook_movable_pos(B_Pos[piece_t][piece], B_Pos, W_Pos))
                    elif "H" in piece:
                        B_movable_poses[piece] = (
                            self.move_functions.get_B_Horse_movable_pos(B_Pos[piece_t][piece], B_Pos, W_Pos))
                    elif "P" in piece:
                        B_movable_poses[piece] = (
                            self.move_functions.get_B_Pawn_movable_pos(B_Pos[piece_t][piece], B_Pos, W_Pos))
                    else:
                        B_movable_poses[piece] = (
                            self.move_functions.get_B_Bishop_movable_pos(B_Pos[piece_t][piece], B_Pos, W_Pos))

            else:
                if "Minister" in piece_t:
                    B_movable_poses[piece_t] = (
                        self.move_functions.get_B_Minister_movable_pos(B_Pos[piece_t], B_Pos, W_Pos))
        B_movable_poses["Black King"] = (
            self.move_functions.get_B_King_movable_pos(self.get_pos_for_piece("Black", "Black King", B_Pos, W_Pos),
                                                       B_Pos, W_Pos))

        return B_movable_poses

    def get_all_W_movable_poses(self, B_Pos, W_Pos):
        W_movable_poses = {}
        for piece_t in W_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in W_Pos[piece_t]:
                    if "R" in piece:
                        W_movable_poses[piece] = (
                            self.move_functions.get_W_Rook_movable_pos(W_Pos[piece_t][piece], B_Pos, W_Pos))
                    elif "H" in piece:
                        W_movable_poses[piece] = (
                            self.move_functions.get_W_Horse_movable_pos(W_Pos[piece_t][piece], B_Pos, W_Pos))
                    elif "P" in piece:
                        W_movable_poses[piece] = (
                            self.move_functions.get_W_Pawn_movable_pos(W_Pos[piece_t][piece], B_Pos, W_Pos))
                    else:
                        W_movable_poses[piece] = (
                            self.move_functions.get_W_Bishop_movable_pos(W_Pos[piece_t][piece], B_Pos, W_Pos))

            else:
                if "Minister" in piece_t:
                    W_movable_poses[piece_t] = (
                        self.move_functions.get_W_Minister_movable_pos(W_Pos[piece_t], B_Pos, W_Pos))
        W_movable_poses["White King"] = (
            self.move_functions.get_W_King_movable_pos(self.get_pos_for_piece("White", "White King", B_Pos, W_Pos),
                                                       B_Pos, W_Pos))
        return W_movable_poses

    def get_pos_for_piece(self, color, name, B_Pos, W_Pos):
        pos = ()
        if color == "Black":
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if name == piece:
                            pos = B_Pos[piece_t][piece]
                            break
                else:
                    if name == piece_t:
                        pos = B_Pos[piece_t]
                        break

        else:
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if name == piece:
                            pos = W_Pos[piece_t][piece]
                            break
                else:
                    if name == piece_t:
                        pos = W_Pos[piece_t]
                        break

        return pos

    def get_piece_for_pos(self, B_Pos, W_Pos, pos):
        piece_type = None
        for piece_t in B_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in B_Pos[piece_t]:
                    if pos == B_Pos[piece_t][piece]:
                        piece_type = piece_t
                        break
            else:
                if pos == B_Pos[piece_t]:
                    piece_type = piece_t
                    break

        for piece_t in W_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in W_Pos[piece_t]:
                    if pos == W_Pos[piece_t][piece]:
                        piece_type = piece_t
                        break
            else:
                if pos == W_Pos[piece_t]:
                    piece_type = piece_t
                    break
        return piece_type

    def get_movable_pos(self, color, pos):
        movable_pos = []
        int_pos = (pos[0] - 1) + (pos[1] - 1) * 8
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]
        current_pos = letters[pos[0] - 1] + str(pos[1])
        if chess.BaseBoard.color_at(self.board, int_pos) is not None:
            if color == "Black":
                for col in letters:
                    for row in range(1, 9):
                        if current_pos != col + str(row):
                            move = chess.Move.from_uci(current_pos + col + str(row))
                            if move in self.board.legal_moves:
                                move_pos = (letters.index(col) + 1, row)
                                movable_pos.append(move_pos)
            else:
                for col in letters:
                    for row in range(1, 9):
                        if current_pos != col + str(row):
                            move = chess.Move.from_uci(current_pos + col + str(row))
                            #move_promotion = chess.Move.from_uci(current_pos + col + str(row) + 'Q')
                            if move in self.board.legal_moves:
                                move_pos = (letters.index(col) + 1, row)
                                movable_pos.append(move_pos)
                            '''elif move_promotion in self.board.legal_moves:
                                print('possible')'''
        return movable_pos

    def draw_dot_or_square(self, color):
        if color == "White":
            for x in self.movable_pos:
                if self.inside_black_pos(x):
                    pos = self.square_to_pix(x[0], x[1], self.border_space)
                    pygame.draw.rect(self.screen, RED, (pos[0], pos[1], 65, 65), 3)

                else:
                    pos = self.square_to_pix(x[0], x[1], self.border_space)
                    self.screen.blit(self.dot, pos)
        else:
            for x in self.movable_pos:
                if self.inside_white_pos(x):
                    pos = self.square_to_pix(x[0], x[1], self.border_space)
                    pygame.draw.rect(self.screen, RED, (pos[0], pos[1], 65, 65), 3)

                else:
                    pos = self.square_to_pix(x[0], x[1], self.border_space)
                    self.screen.blit(self.dot, pos)

    def inside_black_pos(self, check_pos):
        pos = (check_pos[0] - 1) + (check_pos[1] - 1) * 8
        t_or_f = chess.BaseBoard.color_at(self.board, pos)
        if t_or_f is not None:
            return not t_or_f
        else:
            return False

    def inside_white_pos(self, check_pos):
        pos = (check_pos[0] - 1) + (check_pos[1] - 1) * 8
        t_or_f = chess.BaseBoard.color_at(self.board, pos)
        if t_or_f is not None:
            return t_or_f
        else:
            return False

    def move_piece(self):
        if self.selected_piece_colour == "Black":
            for piece_t in self.B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in self.B_Pos[piece_t]:
                        if self.selected_piece == piece:
                            self.B_Pos[piece_t][piece] = self.clicked_board_pos
                            break
                else:
                    if self.selected_piece == piece_t:
                        self.B_Pos[piece_t] = self.clicked_board_pos
                        break

        else:
            for piece_t in self.W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in self.W_Pos[piece_t]:
                        if self.selected_piece == piece:
                            self.record_move(self.W_Pos[piece_t][piece], self.clicked_board_pos)
                            self.W_Pos[piece_t][piece] = self.clicked_board_pos
                            break
                else:
                    if self.selected_piece == piece_t:
                        self.record_move(self.W_Pos[piece_t], self.clicked_board_pos)
                        self.W_Pos[piece_t] = self.clicked_board_pos
                        break

    def cut(self):
        if self.whose_turn == "White":
            B_Pos_Copy = copy.deepcopy(self.B_Pos)
            for piece_t in B_Pos_Copy:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos_Copy[piece_t]:
                        if self.clicked_board_pos == B_Pos_Copy[piece_t][piece]:
                            self.B_Pos[piece_t].pop(piece)
                else:
                    if self.clicked_board_pos == B_Pos_Copy[piece_t]:
                        self.B_Pos.pop(piece_t)

        else:
            W_Pos_Copy = copy.deepcopy(self.W_Pos)
            for piece_t in W_Pos_Copy:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos_Copy[piece_t]:
                        if self.clicked_board_pos == W_Pos_Copy[piece_t][piece]:
                            self.W_Pos[piece_t].pop(piece)
                else:
                    if self.clicked_board_pos == W_Pos_Copy[piece_t]:
                        self.W_Pos.pop(piece_t)

    def find_pins_and_checks(self, B_Pos, W_Pos, colour):
        pins = []
        checks = []
        in_check = False
        if colour == "White":
            enemy_colour = "Black"
            ally_colour = "White"
            pos = self.get_pos_for_piece("White", "White King", B_Pos, W_Pos)
            start_row, start_col = pos[0], pos[1]
        else:
            enemy_colour = "White"
            ally_colour = "Black"
            pos = self.get_pos_for_piece("Black", "Black King", B_Pos, W_Pos)
            start_row, start_col = pos[0], pos[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 < end_row <= 8 and 0 < end_col <= 8:
                    end_piece_type = self.get_piece_for_pos(B_Pos, W_Pos, (end_row, end_col))
                    if end_piece_type is not None:
                        if ally_colour in end_piece_type:
                            if possible_pin == ():
                                possible_pin = (end_row, end_col, d[0], d[1])
                            else:
                                break
                        elif enemy_colour in end_piece_type:
                            if ally_colour == "Black" and end_piece_type == "White Pawn":
                                pass

                            if (0 <= j <= 3 and "Rook" in end_piece_type) or \
                                    (4 <= j <= 7 and "Bishop" in end_piece_type) or \
                                    ((i == 1 and "Pawn" in end_piece_type) and (
                                            (enemy_colour == "White" and 4 <= j <= 5) or (
                                            enemy_colour == "Black" and 6 <= j <= 7))) or \
                                    ("Minister" in end_piece_type) or \
                                    (i == 1 and "King" in end_piece_type):
                                if possible_pin == ():
                                    in_check = True
                                    checks.append((end_row, end_col, d[0], d[1]))
                                    break
                                else:
                                    pins.append(possible_pin)
                                    break
                            else:
                                break
                else:
                    break

        # Checking for horse checks.
        horse_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in horse_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 < end_row <= 8 and 0 < end_col <= 8:
                end_piece_type = self.get_piece_for_pos(B_Pos, W_Pos, (end_row, end_col))
                if end_piece_type is not None:
                    if enemy_colour in end_piece_type and "Horse" in end_piece_type:
                        in_check = True
                        checks.append((end_row, end_col, m[0], m[1]))
        return pins, checks, in_check

    def is_checkmate(self, B_Pos, W_Pos, all_movable_poses, colour):
        pins, checks, in_check = self.find_pins_and_checks(B_Pos, W_Pos, colour)
        if colour == "White":
            if in_check and all(value == [] for value in all_movable_poses.values()):
                print("CHECKMATE!!!!! WHITE")
                return True
        else:
            if in_check and all(value == [] for value in all_movable_poses.values()):
                print("CHECKMATE!!!!! BLACK")
                return True
        return False

    def special_moves(self, B_Pos, W_Pos, color):
        # Pawn reaching opponent's last line.
        if color == "White":
            W_Pos_Copy = copy.deepcopy(W_Pos)
            for piece_t in W_Pos_Copy["White Pawn"]:
                if W_Pos_Copy["White Pawn"][piece_t][1] == 8:
                    del W_Pos["White Pawn"][piece_t]
                    name = "White Minister " + str(piece_t[-1])
                    W_Pos[name] = W_Pos_Copy["White Pawn"][piece_t]
            return W_Pos
        else:
            B_Pos_Copy = copy.deepcopy(B_Pos)
            for piece_t in B_Pos_Copy["Black Pawn"]:
                if B_Pos_Copy["Black Pawn"][piece_t][1] == 1:
                    del B_Pos["Black Pawn"][piece_t]
                    name = "Black Minister " + str(piece_t[-1])
                    B_Pos[name] = B_Pos_Copy["Black Pawn"][piece_t]
            return B_Pos

    def find_direction(self, piece_pos, move_pos):
        x_dir = 0
        y_dir = 0
        if move_pos[0] > piece_pos[0]:
            x_dir = 1
        elif move_pos[0] < piece_pos[0]:
            x_dir = -1

        if move_pos[1] > piece_pos[1]:
            y_dir = 1
        elif move_pos[1] < piece_pos[1]:
            y_dir = -1

        direction = (x_dir, y_dir)
        return direction

    def get_refined_poses(self, movable_poses):
        movable_poses_copy = copy.deepcopy(movable_poses)
        for val in movable_poses_copy:
            if not movable_poses_copy[val]:
                del movable_poses[val]

        return movable_poses

    def get_score(self, positions):
        score = 0
        for piece_t in positions:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in positions[piece_t]:
                    if piece[-2] == "B":
                        score += 30
                    elif piece[-2] == "H":
                        score += 30
                        if positions[piece_t][piece] == (3, 6) or positions[piece_t][piece] == (6, 6):
                            score += 1
                    elif piece[-2] == "R":
                        score += 50
                    elif piece[-2] == "P":
                        score += 10
                        if positions[piece_t][piece][1] == 5:
                            score += 1
            else:
                if "Minister" in piece_t:
                    score += 90
        return score

    def auto_move(self, selected_piece, pos):
        for piece_t in self.B_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in self.B_Pos[piece_t]:
                    if selected_piece == piece:
                        self.record_move(self.B_Pos[piece_t][piece], pos)
                        self.B_Pos[piece_t][piece] = pos
                        break
            else:
                if selected_piece == piece_t:
                    self.record_move(self.B_Pos[piece_t], pos)
                    self.B_Pos[piece_t] = pos
                    break
        W_Pos_Copy = copy.deepcopy(self.W_Pos)
        for piece_t in W_Pos_Copy:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in W_Pos_Copy[piece_t]:
                    if pos == W_Pos_Copy[piece_t][piece]:
                        self.W_Pos[piece_t].pop(piece)
            else:
                if pos == W_Pos_Copy[piece_t]:
                    self.W_Pos.pop(piece_t)

    def record_move(self, start_pos, end_pos):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]
        move = str(letters[start_pos[0] - 1]) + str(start_pos[1]) + str(letters[end_pos[0] - 1]) + str(end_pos[1])
        self.moves_till_now.append(move)

        move_on_board = chess.Move.from_uci(move)
        self.board.push(move_on_board)

    def FindBestMove(self, moves_till_now):
        self.stockfish.set_position(moves_till_now)
        return self.stockfish.get_best_move()

    def fluid_move(self, from_pos, to_pos):
        pieces = {'k': self.B_King,
                  'q': self.B_Minister,
                  'r': self.B_Rook,
                  'b': self.B_Bishop,
                  'n': self.B_Horse,
                  'p': self.B_Pawn,
                  'K': self.W_King,
                  'Q': self.W_Minister,
                  'R': self.W_Rook,
                  'B': self.W_Bishop,
                  'N': self.W_Horse,
                  'P': self.W_Pawn,
                  }
        x1, y1 = self.square_to_pix(from_pos[0], from_pos[1], self.border_space)[0], \
                 self.square_to_pix(from_pos[0], from_pos[1], self.border_space)[1]
        x2, y2 = self.square_to_pix(to_pos[0], to_pos[1], self.border_space)[0], \
                 self.square_to_pix(to_pos[0], to_pos[1], self.border_space)[1]

        try:
            m = (y1 - y2) / (x1 - x2)
        except:
            m = 0

        d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        c = y1 - x1 * m

        if x1 != x2:
            if (x2 - x1) <= 0:
                NorP = round(-(d / 30))
            else:
                NorP = round(d / 30)

            for x3 in range(x1, x2, NorP):
                y3 = round(m * x3 + c)
                self.screen.fill(BLACK)
                self.screen.blit(self.chess_board, (0, 0))
                for i in range(0, 64):
                    piece = str(self.board.piece_at(i))
                    if piece != "None" and self.convert_int_to_pos(i) != from_pos:
                        if (i + 1) % 8 != 0:
                            x = (i + 1) % 8
                            y = ((i + 1) // 8) + 1
                        else:
                            x = 8
                            y = (i + 1) // 8
                        pos = self.square_to_pix(x, y, self.border_space)
                        self.screen.blit(pieces[piece], pos)
                self.screen.blit(pieces[str(self.board.piece_at(self.convert_pos_to_int(from_pos)))], (x3, y3))
                pygame.display.update()
        else:
            if (y2 - y1) <= 0:
                NorP = round(-(d / 30))
            else:
                NorP = round(d / 30)

            for y3 in range(y1, y2, NorP):
                try:
                    x3 = round((y3 - c) / m)
                except:
                    x3 = x1
                self.screen.fill(BLACK)
                self.screen.blit(self.chess_board, (0, 0))
                for i in range(0, 64):
                    piece = str(self.board.piece_at(i))
                    if piece != "None" and self.convert_int_to_pos(i) != from_pos:
                        if (i + 1) % 8 != 0:
                            x = (i + 1) % 8
                            y = ((i + 1) // 8) + 1
                        else:
                            x = 8
                            y = (i + 1) // 8
                        pos = self.square_to_pix(x, y, self.border_space)
                        self.screen.blit(pieces[piece], pos)
                self.screen.blit(pieces[str(self.board.piece_at(self.convert_pos_to_int(from_pos)))], (x3, y3))
                pygame.display.update()

    def convert_int_to_pos(self, i):
        if (i + 1) % 8 != 0:
            x = (i + 1) % 8
            y = ((i + 1) // 8) + 1
        else:
            x = 8
            y = (i + 1) // 8

        pos = (x, y)
        return pos

    def convert_pos_to_int(self, pos):
        return (pos[0]-1) + (pos[1]-1)*8

    def get_outcome(self):
        outcome = None
        raw_outcome = str(self.board.outcome())
        if "CHECKMATE" in raw_outcome:
            if "winner = False" in raw_outcome:
                outcome = ("Checkmate", "Winner = Black")
            else:
                outcome = ("Checkmate", "Winner = White")
        else:
            if "INSUFFICIENT_MATERIAL" in raw_outcome or "STALEMATE" in raw_outcome or "SEVENTYFIVE_MOVES" in raw_outcome or "THREEFOLD_REPETITION" in raw_outcome or "FIFTY_MOVES" in raw_outcome or "FIVEFOLD_REPETITION" in raw_outcome:
                outcome = ("Draw", "Winner = No one")

        return outcome

####################### REAL CODE ###########################


app = App()
app.run()import pygame
import sys
import copy
from Move_functions import *
from stockfish import Stockfish
import chess
import math
from image_diff import *
from camera import *
import cv2

####################### SETTINGS ###########################


pygame.init()
pygame.display.set_caption("Chess With Achachan")

WIDTH = 578
HEIGHT = 578

BLACK = (0, 0, 0)
RED = (225, 0, 0)
GREEN = (0, 225, 0)
BLUE = (0, 0, 255)
GREY = (107, 107, 107)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (33, 39, 49)
TOP_COLOUR = (240, 240, 240)
GOLDEN = (218, 165, 32)

FPS = 27


####################### APP CLASS ###########################


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.chess_board = pygame.image.load("Chess Board.jpg")
        self.B_King = pygame.image.load("B - King.png")
        self.B_Minister = pygame.image.load("B - Minister.png")
        self.B_Rook = pygame.image.load("B - Rook.png")
        self.B_Bishop = pygame.image.load("B - Bishop.png")
        self.B_Horse = pygame.image.load("B - Horse.png")
        self.B_Pawn = pygame.image.load("B - Pawn.png")
        self.W_King = pygame.image.load("W - King.png")
        self.W_Minister = pygame.image.load("W - Minister.png")
        self.W_Rook = pygame.image.load("W - Rook.png")
        self.W_Bishop = pygame.image.load("W - Bishop.png")
        self.W_Horse = pygame.image.load("W - Horse.png")
        self.W_Pawn = pygame.image.load("W - Pawn.png")
        self.dot = pygame.image.load("Dot.png")
        self.Checkmate_image = pygame.image.load("Checkmate.png")
        self.border_space = 25
        self.mouse_pos = pygame.mouse.get_pos()
        self.box_pos = self.pix_to_square(self.mouse_pos[0], self.mouse_pos[1])
        self.clicked_board_pos = ()
        self.clicked = False
        self.selected_piece = None
        self.piece_type = None
        self.selected_piece_colour = None
        self.movable_pos = []
        self.selected_piece_pos = ()
        self.whose_turn = "White"
        self.checkmate = False
        self.outcome = None
        self.moves_till_now = []
        self.stockfish = Stockfish()
        self.board = chess.Board()
        self.pressed = False
        capture_img("img1.png")
        #self.stockfish.set_elo_rating(100)
        self.B_Pos = {
            "Black King": (5, 8),
            "Black Minister": (4, 8),
            "Black Bishop": {"Black B1": (3, 8), "Black B2": (6, 8)},
            "Black Horse": {"Black H1": (2, 8), "Black H2": (7, 8)},
            "Black Rook": {"Black R1": (1, 8), "Black R2": (8, 8)},
            "Black Pawn": {"Black P1": (1, 7), "Black P2": (2, 7), "Black P3": (3, 7), "Black P4": (4, 7),
                           "Black P5": (5, 7), "Black P6": (6, 7), "Black P7": (7, 7), "Black P8": (8, 7)}
        }
        self.W_Pos = {
            "White King": (5, 1),
            "White Minister": (4, 1),
            "White Bishop": {"White B1": (3, 1), "White B2": (6, 1)},
            "White Horse": {"White H1": (2, 1), "White H2": (7, 1)},
            "White Rook": {"White R1": (1, 1), "White R2": (8, 1)},
            "White Pawn": {"White P1": (1, 2), "White P2": (2, 2), "White P3": (3, 2), "White P4": (4, 2),
                           "White P5": (5, 2), "White P6": (6, 2), "White P7": (7, 2),
                           "White P8": (8, 2)}
        }
        self.B_movable_poses = None
        self.W_movable_poses = None
        self.in_check = False
        self.pins = []
        self.checks = []
        self.move_functions = Move_Functions(self)

    def run(self):
        while self.running and self.outcome is None:
            self.events()
            self.updates()
            self.draw()
            self.clock.tick(FPS)
        print(len(self.moves_till_now))
        if self.outcome is not None:
            if self.outcome[0] == "Checkmate":
                if self.outcome[1] == "Winner = White":
                    time = 0
                    while self.running and time < 1000:
                        time += 1
                        self.events()
                        self.screen.fill(BLACK)
                        self.screen.blit(self.chess_board, (0, 0))
                        self.draw_players()
                        self.screen.blit(self.Checkmate_image, (120, 180))
                        pygame.display.update()
                else:
                    print("White won")
            else:
                print("It is a draw")
            pygame.quit()
        sys.exit()

    def events(self):
        self.clicked = False
        self.pressed = False
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                self.running = False

            if events.type == pygame.MOUSEBUTTONUP:
                self.clicked = True

            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_SPACE:
                    self.pressed = True

        self.mouse_pos = pygame.mouse.get_pos()

    def updates(self):
        if self.whose_turn == "White":
            if self.pressed:
                print('clicking picture and saving as img2.png')
                capture_img("img2.png")
                pos1, pos2 = get_move("img1.png", "img2.png", self.board)
                pos1, pos2 = self.correct_move(pos1, pos2, False)
                print(pos1, pos2)
                letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]

                move = str(letters[pos1[0] - 1]) + str(pos1[1]) + str(letters[pos2[0] - 1]) + str(pos2[1])
                move = chess.Move.from_uci(move)
                if move not in self.board.legal_moves:
                    print("ILLEGAL MOVE!")
                    self.running = False
                    self.run()
                self.fluid_move(pos1, pos2)
                self.record_move(pos1, pos2)
                self.whose_turn = "Black"
                self.outcome = self.get_outcome()

        else:
            if self.whose_turn == "Black":
                self.screen.fill(BLACK)
                self.screen.blit(self.chess_board, (0, 0))
                self.draw_players()
                pygame.display.update()
                self.play_best_move()
                self.outcome = self.get_outcome()
                self.whose_turn = "Black -- Waiting"
            elif self.whose_turn == "Black -- Waiting":
                if self.pressed:
                    print("clicking picture and storing as img1.png")
                    capture_img("img1.png")
                    print("MAKE MOVE")
                    self.whose_turn = "White"

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.chess_board, (0, 0))
        self.draw_players()

        pygame.display.update()

    ####################### HELP FUNCTIONS ###########################

    def play_best_move(self):
        best_move = self.FindBestMove(self.moves_till_now)
        if len(best_move) == 4:
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]
            selected_piece_pos = (letters.index(best_move[0]) + 1, int(best_move[1]))
            pos = (letters.index(best_move[2]) + 1, int(best_move[3]))
            self.fluid_move(selected_piece_pos, pos)
            self.record_move(selected_piece_pos, pos)
        else:
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]
            selected_piece_pos = (letters.index(best_move[0]) + 1, int(best_move[1]))
            pos = (letters.index(best_move[2]) + 1, int(best_move[3]))
            self.fluid_move(selected_piece_pos, pos)
            self.moves_till_now.append(best_move)
            move_on_board = chess.Move.from_uci(best_move)
            self.board.push(move_on_board)

    def convert_square(self, move):
        col = ['8', '7', '6', '5', '4', '3', '2', '1']
        square = (int(col[move[0]-1]) , move[1])
        return square

    def correct_move(self, start_pos, end_pos, from_diff):
        if not from_diff:
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]
            move = str(letters[start_pos[0] - 1]) + str(start_pos[1]) + str(letters[end_pos[0] - 1]) + str(end_pos[1])
            move = chess.Move.from_uci(move)
            if move in self.board.legal_moves:
                return start_pos, end_pos
            else:
                return end_pos, start_pos
        else:
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]
            move = str(letters[start_pos[0] - 1]) + str(start_pos[1]) + str(letters[end_pos[0] - 1]) + str(end_pos[1])
            move = chess.Move.from_uci(move)
            if move in self.board.legal_moves:
                return start_pos, end_pos
            else:
                start_pos, end_pos = end_pos, start_pos
                move = str(letters[start_pos[0] - 1]) + str(start_pos[1]) + str(letters[end_pos[0] - 1]) + str(end_pos[1])
                move = chess.Move.from_uci(move)
                if move in self.board.legal_moves:
                    return start_pos, end_pos
        return None, None


    def draw_grid(self, width, height, cell_width, cell_height, border_space):
        for x in range(9):
            pygame.draw.line(self.screen, RED, ((x * cell_width) + border_space, border_space),
                             ((x * cell_width) + border_space, height + border_space))
        for x in range(9):
            pygame.draw.line(self.screen, RED, (border_space, (x * cell_height) + border_space),
                             (width + border_space, (x * cell_height) + border_space))

    def square_to_pix(self, x, y, border_space):
        modified_y = 8 - (y - 1)
        pix_x = ((x - 1) * 66) + border_space
        pix_y = ((modified_y - 1) * 66) + (border_space + 1)
        coordinates = (pix_x, pix_y)

        return coordinates

    def pix_to_square(self, pix_x, pix_y):
        x = 1 + int((pix_x - 27) / 66)
        if x > 8:
            x = 8
        elif x < 1:
            x = 1

        y = 1 + int((pix_y - 27) / 66)
        y = 8 - (y - 1)
        if y > 8:
            y = 8
        elif y < 1:
            y = 1

        coordinates = (x, y)
        return coordinates

    def draw_players(self):
        pieces = {'k': self.B_King,
                  'q': self.B_Minister,
                  'r': self.B_Rook,
                  'b': self.B_Bishop,
                  'n': self.B_Horse,
                  'p': self.B_Pawn,
                  'K': self.W_King,
                  'Q': self.W_Minister,
                  'R': self.W_Rook,
                  'B': self.W_Bishop,
                  'N': self.W_Horse,
                  'P': self.W_Pawn,
                  }
        for i in range(0, 64):
            piece = str(self.board.piece_at(i))
            if piece != "None":
                if (i + 1) % 8 != 0:
                    x = (i + 1) % 8
                    y = ((i + 1) // 8) + 1
                else:
                    x = 8
                    y = (i + 1) // 8
                pos = self.square_to_pix(x, y, self.border_space)
                self.screen.blit(pieces[piece], pos)

    def draw_box(self, position, selected):
        if selected:
            pix_pos = self.square_to_pix(position[0], position[1], self.border_space)
            pygame.draw.rect(self.screen, GREEN, (pix_pos[0], pix_pos[1], 65, 65), 3)
        else:
            pix_pos = self.square_to_pix(position[0], position[1], self.border_space)
            pygame.draw.rect(self.screen, GOLDEN, (pix_pos[0], pix_pos[1], 65, 65), 3)

    def identify_piece(self):
        piece = None
        for x in self.W_Pos:
            if x == "White Rook" or x == "White Bishop" or x == "White Horse" or x == "White Pawn":
                for i in self.W_Pos[x]:
                    if self.W_Pos[x][i] == self.clicked_board_pos:
                        piece = i
                        self.selected_piece_colour = "White"
                        if x == "White Rook":
                            self.piece_type = "Rook"
                        elif x == "White Bishop":
                            self.piece_type = "Bishop"
                        elif x == "White Horse":
                            self.piece_type = "Horse"
                        else:
                            self.piece_type = "Pawn"

            else:
                if self.clicked_board_pos == self.W_Pos[x]:
                    piece = x
                    self.selected_piece_colour = "White"
                    if x == "White King":
                        self.piece_type = "King"
                    else:
                        self.piece_type = "Minister"

        for x in self.B_Pos:
            if x == "Black Rook" or x == "Black Bishop" or x == "Black Horse" or x == "Black Pawn":
                for i in self.B_Pos[x]:
                    if self.B_Pos[x][i] == self.clicked_board_pos:
                        piece = i
                        self.selected_piece_colour = "Black"
                        if x == "Black Rook":
                            self.piece_type = "Rook"
                        elif x == "Black Bishop":
                            self.piece_type = "Bishop"
                        elif x == "Black Horse":
                            self.piece_type = "Horse"
                        else:
                            self.piece_type = "Pawn"

            else:
                if self.clicked_board_pos == self.B_Pos[x]:
                    piece = x
                    self.selected_piece_colour = "Black"
                    if x == "Black King":
                        self.piece_type = "King"
                    else:
                        self.piece_type = "Minister"

        return piece

    def get_all_valid_movable_poses(self, B_Pos, W_Pos, colour):
        '''legal_moves = self.board.legal_moves()
        if colour == "Black":
            for move in legal_moves:
                pass
        '''
        self.pins, self.checks, self.in_check = self.find_pins_and_checks(B_Pos, W_Pos, colour)
        if colour == "Black":
            king_pos = self.get_pos_for_piece("Black", "Black King", B_Pos, W_Pos)
            king_row = king_pos[0]
            king_col = king_pos[1]
            if self.in_check:
                if len(self.checks) == 1:
                    B_movable_poses = self.move_functions.get_all_B_movable_poses(B_Pos, W_Pos, self.pins)
                    check = self.checks[0]
                    check_row = check[0]
                    check_col = check[1]
                    piece_checking = self.get_piece_for_pos(B_Pos, W_Pos, (check_row, check_col))
                    valid_squares = []
                    if "Horse" in piece_checking:
                        valid_squares = [(check_row, check_col)]
                    else:
                        for i in range(1, 8):
                            valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                            valid_squares.append(valid_square)
                            if valid_square[0] == check_row and valid_square[1] == check_col:
                                break

                    for movable_piece in B_movable_poses:
                        B_movable_poses_copy = copy.deepcopy(B_movable_poses)
                        for move in B_movable_poses_copy[movable_piece]:
                            if "King" not in movable_piece:
                                if not (move[0], move[1]) in valid_squares:
                                    B_movable_poses[movable_piece].remove(move)
                else:
                    B_movable_poses = {
                        "Black King": self.move_functions.get_B_King_movable_pos((king_row, king_col), B_Pos, W_Pos),
                        "Black Pawn": {}
                    }
            else:
                B_movable_poses = self.move_functions.get_all_B_movable_poses(B_Pos, W_Pos, self.pins)

            return B_movable_poses
        else:
            king_pos = self.get_pos_for_piece("White", "White King", B_Pos, W_Pos)
            king_row = king_pos[0]
            king_col = king_pos[1]
            if self.in_check:
                if len(self.checks) == 1:
                    W_movable_poses = self.move_functions.get_all_W_movable_poses(B_Pos, W_Pos, self.pins)
                    check = self.checks[0]
                    check_row = check[0]
                    check_col = check[1]
                    piece_checking = self.get_piece_for_pos(B_Pos, W_Pos, (check_row, check_col))
                    valid_squares = []
                    if "Horse" in piece_checking:
                        valid_squares = [(check_row, check_col)]
                    else:
                        for i in range(1, 8):
                            valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                            valid_squares.append(valid_square)
                            if valid_square[0] == check_row and valid_square[1] == check_col:
                                break
                    for movable_piece in W_movable_poses:
                        W_movable_poses_copy = copy.deepcopy(W_movable_poses)
                        for move in W_movable_poses_copy[movable_piece]:
                            if "King" not in movable_piece:
                                if not (move[0], move[1]) in valid_squares:
                                    W_movable_poses[movable_piece].remove(move)
                else:
                    W_movable_poses = {
                        "White King": self.move_functions.get_W_King_movable_pos((king_row, king_col), B_Pos, W_Pos),
                        "White Pawn": {}
                    }
            else:
                W_movable_poses = self.move_functions.get_all_W_movable_poses(B_Pos, W_Pos, self.pins)

            return W_movable_poses

    def get_all_B_movable_poses(self, B_Pos, W_Pos):
        B_movable_poses = {}
        for piece_t in B_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in B_Pos[piece_t]:
                    if "R" in piece:
                        B_movable_poses[piece] = (
                            self.move_functions.get_B_Rook_movable_pos(B_Pos[piece_t][piece], B_Pos, W_Pos))
                    elif "H" in piece:
                        B_movable_poses[piece] = (
                            self.move_functions.get_B_Horse_movable_pos(B_Pos[piece_t][piece], B_Pos, W_Pos))
                    elif "P" in piece:
                        B_movable_poses[piece] = (
                            self.move_functions.get_B_Pawn_movable_pos(B_Pos[piece_t][piece], B_Pos, W_Pos))
                    else:
                        B_movable_poses[piece] = (
                            self.move_functions.get_B_Bishop_movable_pos(B_Pos[piece_t][piece], B_Pos, W_Pos))

            else:
                if "Minister" in piece_t:
                    B_movable_poses[piece_t] = (
                        self.move_functions.get_B_Minister_movable_pos(B_Pos[piece_t], B_Pos, W_Pos))
        B_movable_poses["Black King"] = (
            self.move_functions.get_B_King_movable_pos(self.get_pos_for_piece("Black", "Black King", B_Pos, W_Pos),
                                                       B_Pos, W_Pos))

        return B_movable_poses

    def get_all_W_movable_poses(self, B_Pos, W_Pos):
        W_movable_poses = {}
        for piece_t in W_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in W_Pos[piece_t]:
                    if "R" in piece:
                        W_movable_poses[piece] = (
                            self.move_functions.get_W_Rook_movable_pos(W_Pos[piece_t][piece], B_Pos, W_Pos))
                    elif "H" in piece:
                        W_movable_poses[piece] = (
                            self.move_functions.get_W_Horse_movable_pos(W_Pos[piece_t][piece], B_Pos, W_Pos))
                    elif "P" in piece:
                        W_movable_poses[piece] = (
                            self.move_functions.get_W_Pawn_movable_pos(W_Pos[piece_t][piece], B_Pos, W_Pos))
                    else:
                        W_movable_poses[piece] = (
                            self.move_functions.get_W_Bishop_movable_pos(W_Pos[piece_t][piece], B_Pos, W_Pos))

            else:
                if "Minister" in piece_t:
                    W_movable_poses[piece_t] = (
                        self.move_functions.get_W_Minister_movable_pos(W_Pos[piece_t], B_Pos, W_Pos))
        W_movable_poses["White King"] = (
            self.move_functions.get_W_King_movable_pos(self.get_pos_for_piece("White", "White King", B_Pos, W_Pos),
                                                       B_Pos, W_Pos))
        return W_movable_poses

    def get_pos_for_piece(self, color, name, B_Pos, W_Pos):
        pos = ()
        if color == "Black":
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if name == piece:
                            pos = B_Pos[piece_t][piece]
                            break
                else:
                    if name == piece_t:
                        pos = B_Pos[piece_t]
                        break

        else:
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if name == piece:
                            pos = W_Pos[piece_t][piece]
                            break
                else:
                    if name == piece_t:
                        pos = W_Pos[piece_t]
                        break

        return pos

    def get_piece_for_pos(self, B_Pos, W_Pos, pos):
        piece_type = None
        for piece_t in B_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in B_Pos[piece_t]:
                    if pos == B_Pos[piece_t][piece]:
                        piece_type = piece_t
                        break
            else:
                if pos == B_Pos[piece_t]:
                    piece_type = piece_t
                    break

        for piece_t in W_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in W_Pos[piece_t]:
                    if pos == W_Pos[piece_t][piece]:
                        piece_type = piece_t
                        break
            else:
                if pos == W_Pos[piece_t]:
                    piece_type = piece_t
                    break
        return piece_type

    def get_movable_pos(self, color, pos):
        movable_pos = []
        int_pos = (pos[0] - 1) + (pos[1] - 1) * 8
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]
        current_pos = letters[pos[0] - 1] + str(pos[1])
        if chess.BaseBoard.color_at(self.board, int_pos) is not None:
            if color == "Black":
                for col in letters:
                    for row in range(1, 9):
                        if current_pos != col + str(row):
                            move = chess.Move.from_uci(current_pos + col + str(row))
                            if move in self.board.legal_moves:
                                move_pos = (letters.index(col) + 1, row)
                                movable_pos.append(move_pos)
            else:
                for col in letters:
                    for row in range(1, 9):
                        if current_pos != col + str(row):
                            move = chess.Move.from_uci(current_pos + col + str(row))
                            #move_promotion = chess.Move.from_uci(current_pos + col + str(row) + 'Q')
                            if move in self.board.legal_moves:
                                move_pos = (letters.index(col) + 1, row)
                                movable_pos.append(move_pos)
                            '''elif move_promotion in self.board.legal_moves:
                                print('possible')'''
        return movable_pos

    def draw_dot_or_square(self, color):
        if color == "White":
            for x in self.movable_pos:
                if self.inside_black_pos(x):
                    pos = self.square_to_pix(x[0], x[1], self.border_space)
                    pygame.draw.rect(self.screen, RED, (pos[0], pos[1], 65, 65), 3)

                else:
                    pos = self.square_to_pix(x[0], x[1], self.border_space)
                    self.screen.blit(self.dot, pos)
        else:
            for x in self.movable_pos:
                if self.inside_white_pos(x):
                    pos = self.square_to_pix(x[0], x[1], self.border_space)
                    pygame.draw.rect(self.screen, RED, (pos[0], pos[1], 65, 65), 3)

                else:
                    pos = self.square_to_pix(x[0], x[1], self.border_space)
                    self.screen.blit(self.dot, pos)

    def inside_black_pos(self, check_pos):
        pos = (check_pos[0] - 1) + (check_pos[1] - 1) * 8
        t_or_f = chess.BaseBoard.color_at(self.board, pos)
        if t_or_f is not None:
            return not t_or_f
        else:
            return False

    def inside_white_pos(self, check_pos):
        pos = (check_pos[0] - 1) + (check_pos[1] - 1) * 8
        t_or_f = chess.BaseBoard.color_at(self.board, pos)
        if t_or_f is not None:
            return t_or_f
        else:
            return False

    def move_piece(self):
        if self.selected_piece_colour == "Black":
            for piece_t in self.B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in self.B_Pos[piece_t]:
                        if self.selected_piece == piece:
                            self.B_Pos[piece_t][piece] = self.clicked_board_pos
                            break
                else:
                    if self.selected_piece == piece_t:
                        self.B_Pos[piece_t] = self.clicked_board_pos
                        break

        else:
            for piece_t in self.W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in self.W_Pos[piece_t]:
                        if self.selected_piece == piece:
                            self.record_move(self.W_Pos[piece_t][piece], self.clicked_board_pos)
                            self.W_Pos[piece_t][piece] = self.clicked_board_pos
                            break
                else:
                    if self.selected_piece == piece_t:
                        self.record_move(self.W_Pos[piece_t], self.clicked_board_pos)
                        self.W_Pos[piece_t] = self.clicked_board_pos
                        break

    def cut(self):
        if self.whose_turn == "White":
            B_Pos_Copy = copy.deepcopy(self.B_Pos)
            for piece_t in B_Pos_Copy:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos_Copy[piece_t]:
                        if self.clicked_board_pos == B_Pos_Copy[piece_t][piece]:
                            self.B_Pos[piece_t].pop(piece)
                else:
                    if self.clicked_board_pos == B_Pos_Copy[piece_t]:
                        self.B_Pos.pop(piece_t)

        else:
            W_Pos_Copy = copy.deepcopy(self.W_Pos)
            for piece_t in W_Pos_Copy:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos_Copy[piece_t]:
                        if self.clicked_board_pos == W_Pos_Copy[piece_t][piece]:
                            self.W_Pos[piece_t].pop(piece)
                else:
                    if self.clicked_board_pos == W_Pos_Copy[piece_t]:
                        self.W_Pos.pop(piece_t)

    def find_pins_and_checks(self, B_Pos, W_Pos, colour):
        pins = []
        checks = []
        in_check = False
        if colour == "White":
            enemy_colour = "Black"
            ally_colour = "White"
            pos = self.get_pos_for_piece("White", "White King", B_Pos, W_Pos)
            start_row, start_col = pos[0], pos[1]
        else:
            enemy_colour = "White"
            ally_colour = "Black"
            pos = self.get_pos_for_piece("Black", "Black King", B_Pos, W_Pos)
            start_row, start_col = pos[0], pos[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 < end_row <= 8 and 0 < end_col <= 8:
                    end_piece_type = self.get_piece_for_pos(B_Pos, W_Pos, (end_row, end_col))
                    if end_piece_type is not None:
                        if ally_colour in end_piece_type:
                            if possible_pin == ():
                                possible_pin = (end_row, end_col, d[0], d[1])
                            else:
                                break
                        elif enemy_colour in end_piece_type:
                            if ally_colour == "Black" and end_piece_type == "White Pawn":
                                pass

                            if (0 <= j <= 3 and "Rook" in end_piece_type) or \
                                    (4 <= j <= 7 and "Bishop" in end_piece_type) or \
                                    ((i == 1 and "Pawn" in end_piece_type) and (
                                            (enemy_colour == "White" and 4 <= j <= 5) or (
                                            enemy_colour == "Black" and 6 <= j <= 7))) or \
                                    ("Minister" in end_piece_type) or \
                                    (i == 1 and "King" in end_piece_type):
                                if possible_pin == ():
                                    in_check = True
                                    checks.append((end_row, end_col, d[0], d[1]))
                                    break
                                else:
                                    pins.append(possible_pin)
                                    break
                            else:
                                break
                else:
                    break

        # Checking for horse checks.
        horse_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in horse_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 < end_row <= 8 and 0 < end_col <= 8:
                end_piece_type = self.get_piece_for_pos(B_Pos, W_Pos, (end_row, end_col))
                if end_piece_type is not None:
                    if enemy_colour in end_piece_type and "Horse" in end_piece_type:
                        in_check = True
                        checks.append((end_row, end_col, m[0], m[1]))
        return pins, checks, in_check

    def is_checkmate(self, B_Pos, W_Pos, all_movable_poses, colour):
        pins, checks, in_check = self.find_pins_and_checks(B_Pos, W_Pos, colour)
        if colour == "White":
            if in_check and all(value == [] for value in all_movable_poses.values()):
                print("CHECKMATE!!!!! WHITE")
                return True
        else:
            if in_check and all(value == [] for value in all_movable_poses.values()):
                print("CHECKMATE!!!!! BLACK")
                return True
        return False

    def special_moves(self, B_Pos, W_Pos, color):
        # Pawn reaching opponent's last line.
        if color == "White":
            W_Pos_Copy = copy.deepcopy(W_Pos)
            for piece_t in W_Pos_Copy["White Pawn"]:
                if W_Pos_Copy["White Pawn"][piece_t][1] == 8:
                    del W_Pos["White Pawn"][piece_t]
                    name = "White Minister " + str(piece_t[-1])
                    W_Pos[name] = W_Pos_Copy["White Pawn"][piece_t]
            return W_Pos
        else:
            B_Pos_Copy = copy.deepcopy(B_Pos)
            for piece_t in B_Pos_Copy["Black Pawn"]:
                if B_Pos_Copy["Black Pawn"][piece_t][1] == 1:
                    del B_Pos["Black Pawn"][piece_t]
                    name = "Black Minister " + str(piece_t[-1])
                    B_Pos[name] = B_Pos_Copy["Black Pawn"][piece_t]
            return B_Pos

    def find_direction(self, piece_pos, move_pos):
        x_dir = 0
        y_dir = 0
        if move_pos[0] > piece_pos[0]:
            x_dir = 1
        elif move_pos[0] < piece_pos[0]:
            x_dir = -1

        if move_pos[1] > piece_pos[1]:
            y_dir = 1
        elif move_pos[1] < piece_pos[1]:
            y_dir = -1

        direction = (x_dir, y_dir)
        return direction

    def get_refined_poses(self, movable_poses):
        movable_poses_copy = copy.deepcopy(movable_poses)
        for val in movable_poses_copy:
            if not movable_poses_copy[val]:
                del movable_poses[val]

        return movable_poses

    def get_score(self, positions):
        score = 0
        for piece_t in positions:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in positions[piece_t]:
                    if piece[-2] == "B":
                        score += 30
                    elif piece[-2] == "H":
                        score += 30
                        if positions[piece_t][piece] == (3, 6) or positions[piece_t][piece] == (6, 6):
                            score += 1
                    elif piece[-2] == "R":
                        score += 50
                    elif piece[-2] == "P":
                        score += 10
                        if positions[piece_t][piece][1] == 5:
                            score += 1
            else:
                if "Minister" in piece_t:
                    score += 90
        return score

    def auto_move(self, selected_piece, pos):
        for piece_t in self.B_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in self.B_Pos[piece_t]:
                    if selected_piece == piece:
                        self.record_move(self.B_Pos[piece_t][piece], pos)
                        self.B_Pos[piece_t][piece] = pos
                        break
            else:
                if selected_piece == piece_t:
                    self.record_move(self.B_Pos[piece_t], pos)
                    self.B_Pos[piece_t] = pos
                    break
        W_Pos_Copy = copy.deepcopy(self.W_Pos)
        for piece_t in W_Pos_Copy:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in W_Pos_Copy[piece_t]:
                    if pos == W_Pos_Copy[piece_t][piece]:
                        self.W_Pos[piece_t].pop(piece)
            else:
                if pos == W_Pos_Copy[piece_t]:
                    self.W_Pos.pop(piece_t)

    def record_move(self, start_pos, end_pos):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', ]
        move = str(letters[start_pos[0] - 1]) + str(start_pos[1]) + str(letters[end_pos[0] - 1]) + str(end_pos[1])
        self.moves_till_now.append(move)

        move_on_board = chess.Move.from_uci(move)
        self.board.push(move_on_board)

    def FindBestMove(self, moves_till_now):
        self.stockfish.set_position(moves_till_now)
        return self.stockfish.get_best_move()

    def fluid_move(self, from_pos, to_pos):
        pieces = {'k': self.B_King,
                  'q': self.B_Minister,
                  'r': self.B_Rook,
                  'b': self.B_Bishop,
                  'n': self.B_Horse,
                  'p': self.B_Pawn,
                  'K': self.W_King,
                  'Q': self.W_Minister,
                  'R': self.W_Rook,
                  'B': self.W_Bishop,
                  'N': self.W_Horse,
                  'P': self.W_Pawn,
                  }
        x1, y1 = self.square_to_pix(from_pos[0], from_pos[1], self.border_space)[0], \
                 self.square_to_pix(from_pos[0], from_pos[1], self.border_space)[1]
        x2, y2 = self.square_to_pix(to_pos[0], to_pos[1], self.border_space)[0], \
                 self.square_to_pix(to_pos[0], to_pos[1], self.border_space)[1]

        try:
            m = (y1 - y2) / (x1 - x2)
        except:
            m = 0

        d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        c = y1 - x1 * m

        if x1 != x2:
            if (x2 - x1) <= 0:
                NorP = round(-(d / 30))
            else:
                NorP = round(d / 30)

            for x3 in range(x1, x2, NorP):
                y3 = round(m * x3 + c)
                self.screen.fill(BLACK)
                self.screen.blit(self.chess_board, (0, 0))
                for i in range(0, 64):
                    piece = str(self.board.piece_at(i))
                    if piece != "None" and self.convert_int_to_pos(i) != from_pos:
                        if (i + 1) % 8 != 0:
                            x = (i + 1) % 8
                            y = ((i + 1) // 8) + 1
                        else:
                            x = 8
                            y = (i + 1) // 8
                        pos = self.square_to_pix(x, y, self.border_space)
                        self.screen.blit(pieces[piece], pos)
                self.screen.blit(pieces[str(self.board.piece_at(self.convert_pos_to_int(from_pos)))], (x3, y3))
                pygame.display.update()
        else:
            if (y2 - y1) <= 0:
                NorP = round(-(d / 30))
            else:
                NorP = round(d / 30)

            for y3 in range(y1, y2, NorP):
                try:
                    x3 = round((y3 - c) / m)
                except:
                    x3 = x1
                self.screen.fill(BLACK)
                self.screen.blit(self.chess_board, (0, 0))
                for i in range(0, 64):
                    piece = str(self.board.piece_at(i))
                    if piece != "None" and self.convert_int_to_pos(i) != from_pos:
                        if (i + 1) % 8 != 0:
                            x = (i + 1) % 8
                            y = ((i + 1) // 8) + 1
                        else:
                            x = 8
                            y = (i + 1) // 8
                        pos = self.square_to_pix(x, y, self.border_space)
                        self.screen.blit(pieces[piece], pos)
                self.screen.blit(pieces[str(self.board.piece_at(self.convert_pos_to_int(from_pos)))], (x3, y3))
                pygame.display.update()

    def convert_int_to_pos(self, i):
        if (i + 1) % 8 != 0:
            x = (i + 1) % 8
            y = ((i + 1) // 8) + 1
        else:
            x = 8
            y = (i + 1) // 8

        pos = (x, y)
        return pos

    def convert_pos_to_int(self, pos):
        return (pos[0]-1) + (pos[1]-1)*8

    def get_outcome(self):
        outcome = None
        raw_outcome = str(self.board.outcome())
        if "CHECKMATE" in raw_outcome:
            if "winner = False" in raw_outcome:
                outcome = ("Checkmate", "Winner = Black")
            else:
                outcome = ("Checkmate", "Winner = White")
        else:
            if "INSUFFICIENT_MATERIAL" in raw_outcome or "STALEMATE" in raw_outcome or "SEVENTYFIVE_MOVES" in raw_outcome or "THREEFOLD_REPETITION" in raw_outcome or "FIFTY_MOVES" in raw_outcome or "FIVEFOLD_REPETITION" in raw_outcome:
                outcome = ("Draw", "Winner = No one")

        return outcome

####################### REAL CODE ###########################


app = App()
app.run()

# Currently I have given self.B_movable_poses. Change to B_movable_poses!!!
# Develop King movable positions!!!
# Change pawn-check checking part ------- IMP
# Change pawn vertical checks ----------------IMP
# Change check to reduce work load.


# Currently I have given self.B_movable_poses. Change to B_movable_poses!!!
# Develop King movable positions!!!
# Change pawn-check checking part ------- IMP
# Change pawn vertical checks ----------------IMP
# Change check to reduce work load.
