import pygame
import sys
import chess
import copy
from stockfish import Stockfish

# --- Constants ---
WIDTH = 800
HEIGHT = 800
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
IMAGES = {}  # Dictionary to hold loaded piece images
COLORS = [ (240,217,181), (181,136,99)]  #Light and dark squares

# --- Load Images ---
def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) # replace with your own images
        print(f"Loaded image: {piece}")

# --- Main Function ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()
    running = True
    load_images() #Load images
    game_state = GameState()
    stockfish = Stockfish(path="/opt/homebrew/bin/stockfish") # change to your stockfish bin path
    #stockfish = Stockfish() # if it does not work on windows
    valid_moves = game_state.get_valid_moves()
    move_made = False # flag variable for when a move is made

    sq_selected = () # no square selected initially, this is a tuple: (row, col)
    player_clicks = [] # keep track of player clicks (two tuples: [(6,4), (4,4)])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #Mouse handler
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() #(x, y)
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col): # the user clicked the same square twice
                    sq_selected = () # deselect
                    player_clicks = [] # clear player clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected) # append for both 1st and 2nd click
                if len(player_clicks) == 2: # after 2nd click
                    move = Move(player_clicks[0], player_clicks[1], game_state.board)
                    print(move.get_chess_notation())

                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            game_state.make_move(valid_moves[i])
                            move_made = True
                            sq_selected = () #reset user clicks
                            player_clicks = []
                    if not move_made:
                        player_clicks = [sq_selected]

            #Key handler
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: # undo when 'z' is pressed
                    game_state.undo_move()
                    move_made = True


        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False

        #AI move
        if game_state.white_to_move == False:
          stockfish.set_fen_position(game_state.board.fen())
          engine_move = stockfish.get_best_move()

          if engine_move is not None: # Engine move available
            move = chess.Move.from_uci(engine_move)
            for valid_move in valid_moves:
              # This is really important to ensure you make a legal move
              if valid_move.move == move:
                game_state.make_move(valid_move)
                move_made = True

        if game_state.checkmate:
          font = pygame.font.Font(None, 72)
          if game_state.white_to_move:
            text = font.render("Black Wins", True, (0,0,0)) #display it
          else:
            text = font.render("White Wins", True, (0,0,0)) #display it
          text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
          screen.blit(text, text_rect)
          pygame.display.flip() # show display
          pygame.time.wait(3000) #display 3 seconds
          running = False

        draw_game_state(screen, game_state, sq_selected, valid_moves)
        clock.tick(15)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# --- Game State Class ---
class GameState():
    def __init__(self):
        self.board = chess.Board()
        self.move_log = []
        self.white_to_move = True
        self.white_king_location = (7,4)
        self.black_king_location = (0,4)
        self.white_in_check = False
        self.black_in_check = False
        self.pins = []
        self.checks = []
        self.checkmate = False

    def make_move(self, move):

        self.board.push(move.move) #Now make move on board
        self.move_log.append(move) #log move

        self.white_to_move = not self.white_to_move #switch player

        if str(move.move).find('king') != -1: #check the location
            self.update_king_locations(move)

        inCheck, pins, checks = self.check_for_pins_and_checks()

        if len(checks) > 0 :
            self.checkmate = self.checkForCheckMate()
            #The move causes checkmate - handle

        else: self.checkmate = False

    def undo_move(self):
        if self.move_log: # make sure that there is a move to undo
            move = self.move_log.pop() #pop last move off of move log
            self.board.pop() #undo move on board
            self.white_to_move = not self.white_to_move #switch players

    def update_king_locations(self, move): #Updat the postion
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

    def get_valid_moves(self):
        return self.get_all_possible_moves() # for now we will not worry about checks

    def get_all_possible_moves(self):
        moves = []
        for i in range(64):
            row = i // 8
            col = i % 8
            piece = self.board.piece_at(i)
            if piece is not None:
                turn = 'w' if self.white_to_move else 'b'
                if piece.color == (self.white_to_move): # right color
                    piece = piece.symbol()
                    if piece.startswith(turn): # if turn and color matches
                        for move in self.board.legal_moves:
                            if (move.from_square == i):
                                start_row = move.from_square // 8
                                start_col = move.from_square % 8

                                end_row = move.to_square // 8
                                end_col = move.to_square % 8

                                move_obj = Move((start_row, start_col), (end_row, end_col), self.board)
                                moves.append(move_obj)
        return moves

    def check_for_pins_and_checks(self):
        pins = [] # squares where the allied pinned piece is and direction pinned from
        checks = [] # sqaures where enemy is applying a check
        inCheck = False

        if self.white_to_move:
          enemyColor = 'b'
          allyColor = 'w'
          startRow = self.white_king_location[0]
          startCol = self.white_king_location[1]
        else:
          enemyColor = 'w'
          allyColor = 'b'
          startRow = self.black_king_location[0]
          startCol = self.black_king_location[1]
        
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
          d = directions[j]
          possiblePin = () # reset possible pins
          for i in range(8):
            endRow = startRow + d[0] * (i+1)
            endCol = startCol + d[1] * (i+1)
            if 0 <= endRow < 8 and 0 <= endCol < 8:
              endPiece = self.board.piece_at(endRow*8 + endCol) # convert row,col to a number between 0-63
              if endPiece is not None:
                endPiece = endPiece.symbol()
                if endPiece.startswith(allyColor) and possiblePin == (): # 1st allied piece
                  possiblePin = (endRow, endCol, d[0], d[1])
                elif endPiece.startswith(enemyColor): # 2nd piece - or enemy

                  ### NEEDED TO ADD A AND D TO THE LIST

                  type = endPiece[1]
                  if (0 <= j <= 3 and type == 'R') or \
                      (4 <= j <= 7 and type == 'B') or \
                      (i == 0 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                      (type == 'Q') or (i == 0 and type == 'K'): # can check to see if conditions above apply to this area!

                        if possiblePin == (): # there is no blocking piece so check
                          inCheck = True
                          checks.append((endRow, endCol, d[0], d[1]))
                          break
                        else: # only 1 allied piece blocking so pin
                          pins.append(possiblePin)
                          break
                else: # 3rd space empty then we can move on
                  break
            else:
              break # off board
        
        # now check if a knight is creating a check
        knightMoves = ((-2, -1), (-2, 1), (-1, 2), (-1, -2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
          endRow = startRow + m[0]
          endCol = startCol + m[1]

          if 0 <= endRow < 8 and 0 <= endCol < 8:
            endPiece = self.board.piece_at(endRow*8+endCol) # convert row,col to a number between 0-63
            if endPiece is not None:
              endPiece = endPiece.symbol()
              if endPiece.startswith(enemyColor) and endPiece[1] == "N": #enemy knight attaking king
                  inCheck = True
                  checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    def checkForCheckMate(self):
      validMoves = self.get_valid_moves()
      if len(validMoves) == 0:
        return True # if the player has no moves
      else:
        return False #The player has avialable moves

# --- Move Class ---
class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]

        start = self.start_row * 8 + self.start_col
        end = self.end_row * 8 + self.end_col

        self.move = chess.Move(start, end)

        self.piece_moved = board.piece_at(start).symbol() # type: ignore

    '''Override equals method'''
    def __eq__(self, other): # compares each attribute to determine if they are similar - i.e. if they are the same move
        if isinstance(other, Move):
            return self.start_row == other.start_row and self.start_col == other.start_col and self.end_row == other.end_row and self.end_col == other.end_col
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]

# --- Drawing Functions ---
def draw_game_state(screen, game_state, sq_selected, valid_moves):
    draw_board(screen)  # Draw squares on the board
    highlight_squares(screen, game_state, sq_selected, valid_moves)
    draw_pieces(screen, game_state.board) #Draw pieces on top of the squares

def draw_board(screen):
  for row in range(DIMENSION):
    for col in range(DIMENSION):
        color = COLORS[(row + col) % 2]
        pygame.draw.rect(screen, color, pygame.Rect(col* SQ_SIZE, row* SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlight_squares(screen, game_state, sq_selected, valid_moves):
    if sq_selected != ():
      row, col = sq_selected

      for move in valid_moves:
        #Light up the square the piece can be moved to
        if move.start_row == row and move.start_col == col:
          s = pygame.Surface((SQ_SIZE, SQ_SIZE))
          s.set_alpha(100) #Transparency value -> 0 transparent, 255 opaque
          s.fill(pygame.Color('blue'))
          screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))

      #Light up the selected square
      s = pygame.Surface((SQ_SIZE, SQ_SIZE))
      s.set_alpha(100) #Transparency value -> 0 transparent, 255 opaque
      s.fill(pygame.Color('blue'))
      screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board.piece_at(row*8 + col)
            if piece is not None:
                screen.blit(IMAGES[piece.symbol()], pygame.Rect(col* SQ_SIZE, row* SQ_SIZE, SQ_SIZE, SQ_SIZE))

# --- Run the game ---
if __name__ == "__main__":
    main()
