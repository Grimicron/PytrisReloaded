import pygame
import random
import time

################################
# UTILITY CLASSES
################################


# Makes gfx calc easier
class vec:
    def __init__(self, px, py):
        self.x = px
        self.y = py

    def add(self, v):
        return vec(self.x + v.x, self.y + v.y)

    def sub(self, v):
        return vec(self.x - v.x, self.y - v.y)

    def mult(self, scalar):
        return vec(self.x * scalar, self.y * scalar)


class drawing_manager:
    @staticmethod
    def interpret_color(color):
        if color == "blue":
            return (0, 0, 255)
        elif color == "aqua":
            return (0, 255, 255)
        elif color == "red":
            return (255, 0, 0)
        elif color == "green":
            return (0, 255, 0)
        elif color == "yellow":
            return (255, 255, 0)
        elif color == "purple":
            return (153, 0, 255)
        elif color == "orange":
            return (255, 153, 0)
        # Just in case the color is not valid it will return white so you know
        # there is something wrong with the piece
        return (255, 255, 255)

    @staticmethod
    def draw_piece(pos, piece_state, color):
        for i in range(4):
            for j in range(4):
                if piece_state[i][j] == "X":
                    drawing_manager.draw_box(
                        vec(j, i).add(pos).mult(BOX_SIZE).add(BOARD_POS),
                        drawing_manager.interpret_color(color))

    def draw_dead_pieces(pieces):
        for i in range(20):
            for j in range(10):
                if pieces[i][j] != "":
                    drawing_manager.draw_box(
                        # Not sure about why I have to have the +1
                        vec(j, i+1).mult(BOX_SIZE).add(BOARD_POS),
                        drawing_manager.interpret_color(pieces[i][j]))

    @staticmethod
    def draw_box(pos, color):
        pygame.draw.rect(SCREEN, color,
                         pygame.Rect(pos.x, pos.y, BOX_SIZE, BOX_SIZE))

    @staticmethod
    def draw_bg():
        pygame.draw.rect(SCREEN, (255, 255, 255),
                         pygame.Rect(0, 0, SCREEN_SIZE.x, SCREEN_SIZE.y))
        #                 Not sure why I have to have this BOX_SIZE |
        #                                                           V
        pygame.draw.rect(
            SCREEN, (0, 0, 0),
            pygame.Rect(BOARD_POS.x, BOARD_POS.y + BOX_SIZE, 10 * BOX_SIZE,
                        20 * BOX_SIZE))


################################
# CONSTANTS
################################

BOX_SIZE = 15
BOARD_POS = vec(150, 50)
SCREEN_SIZE = vec(500, 500)
SCREEN = pygame.display.set_mode([SCREEN_SIZE.x, SCREEN_SIZE.y])
GRAVITY = 2.0
DAS = 4.0
# FAST_MULTIPLIER cannot be one
FAST_MULTIPLIER = 2.0
# Adding to the piece state rotates the piece clockwise
O_PIECE = ([["....", ".XX.", ".XX.", "...."], ["....", ".XX.", ".XX.", "...."],
            ["....", ".XX.", ".XX.", "...."], ["....", ".XX.", ".XX.", "...."]], "blue")
T_PIECE = ([["....", ".XXX", "..X.", "...."], ["..X.", ".XX.", "..X.", "...."],
            ["..X.", ".XXX", "....", "...."], ["..X.", "..XX", "..X.", "...."]], "green")
I_PIECE = ([["..X.", "..X.", "..X.", "..X."], ["....", "....", "XXXX", "...."],
            [".X..", ".X..", ".X..", ".X.."], ["....", "XXXX", "....", "...."]], "red")
Z_PIECE = ([["....", ".XX.", "..XX", "...."], ["..X.", ".XX.", ".X..", "...."],
            ["....", ".XX.", "..XX", "...."], ["..X.", ".XX.", ".X..", "...."]], "orange")
S_PIECE = ([["....", "..XX", ".XX.", "...."], [".X..", ".XX.", "..X.", "...."],
            ["....", "..XX", ".XX.", "...."], [".X..", ".XX.", "..X.", "...."]], "aqua")
J_PIECE = ([["..X.", "..X.", ".XX.", "...."], ["....", ".X..", ".XXX", "...."],
            [".XX.", ".X..", ".X..", "...."], ["....", "...X", ".XXX", "...."]], "yellow")
L_PIECE = ([[".X..", ".X..", ".XX.", "...."], ["....", "..X.", "XXX.", "...."],
            [".XX.", "..X.", "..X.", "...."], ["....", "X...", "XXX.", "...."]], "purple")
PIECES = [O_PIECE, T_PIECE, I_PIECE, Z_PIECE, S_PIECE, J_PIECE, L_PIECE]

################################
# GAME CLASSES
################################


class piece:
    def __init__(self, piece_info):
        self.states = piece_info[0]
        # Some pieces begin at the first row and other at the second
        # so with this if we ensure that the pieces begin at the very top
        self.pos = vec(3, 1 if "X" in self.states[0][0] else 0)
        self.current_state = 0
        self.color = piece_info[1]

    def draw(self):
        drawing_manager.draw_piece(self.pos, self.states[self.current_state],
                                   self.color)
        
    # Just to make code cleaner later on
    def get_state(self, shift=0):
        return self.states[(self.current_state+shift)%4]

class dead_pieces:
    data = []
    fast = False

    @staticmethod
    def init():
        for i in range(20):
            dead_pieces.data.append([])
            for j in range(10):
                dead_pieces.data[i].append("")

    @staticmethod
    def draw():
        drawing_manager.draw_dead_pieces(dead_pieces.data)

    @staticmethod
    def add_piece(pos, state, color):
        pos.y -= 1
        for i in range(4):
            for j in range(4):
                if state[i][j] == "X":
                    dead_pieces.data[pos.y + i][pos.x + j] = color

    @staticmethod
    def clear_line(line):
        for i in reversed(range(0, line)):
            if i == 0:
                dead_pieces.data[i] = [""] * 10
                continue
            for j in range(10):
                dead_pieces.data[i][j] = dead_pieces.data[i - 1][j]

    @staticmethod
    def clear_lines():
        for i in range(20):
            full = True
            for j in range(10):      
                if dead_pieces.data[i][j] == "":
                    full = False
                    break
            if full:
                dead_pieces.clear_line(i)

    @staticmethod
    def colliding(pos, state):
        for i in range(4):
            if pos.y+i >= 20:
                return
            for j in range(4):
                if pos.x+j >= 10:
                    # Same thing here except we only break because we still need to check
                    # the other heights
                    break
                if state[i][j] == "X":
                    if dead_pieces.data[pos.y + i][pos.x + j] != '':
                        return True
        return False

class game:
    player_piece = None
    fps_ts = 0
    das_ts = 0

    @staticmethod
    def can_move(pos, state):
        for i in range(4):
            for j in range(4):
                if state[i][j] == "X":
                    if pos.x+j < 0:
                        print("left")
                        return False
                    if pos.x+j >= 10:
                        print("right")
                        return False
                    if pos.y+i >= 20:
                        print("floor")
                        return False
        if dead_pieces.colliding(pos, state):
            return False
        return True

    @staticmethod
    def try_rotate(clockwise):
        if clockwise:
            if not(game.can_move(game.player_piece.pos, game.player_piece.get_state(1))):
                return
            game.player_piece.current_state += 1
            game.player_piece.current_state %= 4
        else:
            if not(game.can_move(game.player_piece.pos, game.player_piece.get_state(-1))):
                return
            game.player_piece.current_state -= 1
            game.player_piece.current_state %= 4
            
    
    @staticmethod
    def player_input():
        keys = pygame.key.get_pressed()
        game.fast = keys[pygame.K_DOWN]
        if keys[pygame.K_LEFT] and (time.time() > game.das_ts):
            if game.can_move(game.player_piece.pos.add(vec(-1, 0))
              ,game.player_piece.get_state()):
                game.player_piece.pos.x += -1
                game.das_ts = time.time() + 1.0 / DAS    
        elif keys[pygame.K_RIGHT] and (time.time() > game.das_ts):
            if game.can_move(game.player_piece.pos.add(vec(1, 0))
              ,game.player_piece.get_state()):
                game.player_piece.pos.x += 1
                game.das_ts = time.time() + 1.0 / DAS

    @staticmethod
    def frame():
        drawing_manager.draw_bg()
        game.player_piece.draw()
        dead_pieces.draw()
        game.player_input()
        if time.time() > (game.fps_ts - 
                          (((FAST_MULTIPLIER-1) / (FAST_MULTIPLIER*GRAVITY) if game.fast else 0))):
            if game.can_move(game.player_piece.pos.add(vec(0, 1))
                              ,game.player_piece.get_state()):
                game.player_piece.pos.y += 1
            else:
                dead_pieces.add_piece(game.player_piece.pos.add(vec(0, 1))
                                     ,game.player_piece.get_state()
                                     ,game.player_piece.color)
                game.player_piece = piece(random.choice(PIECES))
            game.fps_ts = time.time() + 1 / GRAVITY

    @staticmethod
    def start():
        pygame.init()
        game.player_piece = piece(random.choice(PIECES))
        dead_pieces.init()
        game.fps_ts = time.time() + 1 / GRAVITY
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Rotate piece clockwise/counterclockwise
                # done here because this is the only place we can handle
                # events and we want the rotate piece to be
                # a key down event so it only happens once per press
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game.try_rotate(True)
                    elif event.key == pygame.K_LCTRL:
                        game.try_rotate(False)
            game.frame()
            pygame.display.flip()
        pygame.quit()

game.start()
