import pygame
import random

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
                    drawing_manager.draw_box(vec(j, i).add(pos).mult(BOX_SIZE).add(BOARD_POS)
                                            ,drawing_manager.interpret_color(color))

    def draw_dead_pieces(pieces):
        for i in range(20):
            for j in range(10):
                if pieces[i][j] != "":
                    drawing_manager.draw_box(vec(j, i).mult(BOX_SIZE).add(BOARD_POS)
                                            ,drawing_manager.interpret_color(pieces[i][j]))
    
    @staticmethod
    def draw_box(pos, color):
        pygame.draw.rect(screen, color, pygame.Rect(pos.x, pos.y, BOX_SIZE, BOX_SIZE))
    @staticmethod
    def draw_bg():
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, SCREEN_SIZE.x, SCREEN_SIZE.y))
        #                                     Not sure why I have to have this BOX_SIZE |
        #                                                                               V
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(BOARD_POS.x, BOARD_POS.y + BOX_SIZE, 10*BOX_SIZE, 20*BOX_SIZE))

################################
# CONSTANTS
################################
        
BOX_SIZE = 15
BOARD_POS = vec(150, 50)
SCREEN_SIZE = vec(500, 500)
screen = pygame.display.set_mode([SCREEN_SIZE.x, SCREEN_SIZE.y])
# Adding to the piece state rotates the piece clockwise
O_PIECE = ([["....", ".XX.", ".XX.", "...."],
            ["....", ".XX.", ".XX.", "...."],
            ["....", ".XX.", ".XX.", "...."],
            ["....", ".XX.", ".XX.", "...."]], "blue")
T_PIECE = ([["....", ".XXX", "..X.", "...."],
            ["..X.", ".XX.", "..X.", "...."],
            ["..X.", ".XXX", "....", "...."],
            ["..X.", "..XX", "..X.", "...."]], "green")
I_PIECE = ([["..X.", "..X.", "..X.", "..X."],
            ["....", "....", "XXXX", "...."],
            [".X..", ".X..", ".X..", ".X.."],
            ["....", "XXXX", "....", "...."]], "red")
Z_PIECE = ([["....", ".XX.", "..XX", "...."],
            ["..X.", ".XX.", ".X..", "...."],
            ["....", ".XX.", "..XX", "...."],
            ["..X.", ".XX.", ".X..", "...."]], "orange")
S_PIECE = ([["....", "..XX", ".XX.", "...."],
            [".X..", ".XX.", "..X.", "...."],
            ["....", "..XX", ".XX.", "...."],
            [".X..", ".XX.", "..X.", "...."]], "aqua")
J_PIECE = ([["..X.", "..X.", ".XX.", "...."],
            ["....", ".X..", ".XXX", "...."],
            [".XX.", ".X..", ".X..", "...."],
            ["....", "...X", ".XXX", "...."]], "yellow")
L_PIECE = ([[".X..", ".X..", ".XX.", "...."],
            ["....", "..X.", "XXX.", "...."],
            [".XX.", "..X.", "..X.", "...."],
            ["....", "X...", "XXX.", "...."]], "purple")
PIECES = [O_PIECE, T_PIECE, I_PIECE, Z_PIECE, S_PIECE, J_PIECE, L_PIECE]

################################
# PIECE CLASSES
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
        drawing_manager.draw_piece(self.pos, self.states[self.current_state], self.color)

class dead_pieces:
    data = []

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
        for i in range(4):
            for j in  range(4):
                if state[i][j] == "X":
                    dead_pieces.data[pos.x+j][pos.y+i] = color
    
    @staticmethod
    def clear_line(line):
        for i in reversed(range(0, line)):
            if i == 0:
                dead_pieces.data[i] = [""]*10
                continue
            for j in range(10):
                dead_pieces.data[i][j] = dead_pieces.data[i-1][j]

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

class game:
    player_piece = None
    
    @staticmethod
    def frame():
        drawing_manager.draw_bg()
        game.player_piece.draw()
        dead_pieces.draw()
    
    @staticmethod
    def start():
        pygame.init()
        game.player_piece = piece(random.choice(PIECES))
        dead_pieces.init()
        while  True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            game.frame()
        pygame.quit()

game.start()