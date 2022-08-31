import pygame
import random
import time
import math

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
    def draw_piece(pos, piece_state, color):
        for i in range(4):
            for j in range(4):
                if piece_state[i][j] == "X":
                    drawing_manager.draw_box(
                        vec(j, i).add(pos).mult(BOX_SIZE).add(BOARD_POS), COLORS[color])

    def draw_dead_pieces(pieces):
        for i in range(20):
            for j in range(10):
                if pieces[i][j] != "":
                    drawing_manager.draw_box(
                        vec(j, i).mult(BOX_SIZE).add(BOARD_POS), COLORS[pieces[i][j]])

    @staticmethod
    def draw_box(pos, color):
        pygame.draw.rect(SCREEN, color,
                         pygame.Rect(pos.x, pos.y, BOX_SIZE, BOX_SIZE))
        pygame.draw.rect(SCREEN, tuple(min(i+BOX_HIGHLIGHT_AMOUNT, 255) for i in color),
                         pygame.Rect(pos.x, pos.y, math.floor(BOX_SIZE*BOX_LIGHT_PROPORTION), BOX_SIZE))
        pygame.draw.rect(SCREEN, tuple(max(i+BOX_SHADOW_AMOUNT, 0) for i in color),
                         pygame.Rect(pos.x + BOX_SIZE - math.floor(BOX_SIZE*BOX_LIGHT_PROPORTION), pos.y
                                    ,math.floor(BOX_SIZE*BOX_LIGHT_PROPORTION), BOX_SIZE))
        pygame.draw.rect(SCREEN, tuple(max(i+BOX_SHADOW_AMOUNT, 0) for i in color),
                         pygame.Rect(pos.x, pos.y + BOX_SIZE - math.floor(BOX_SIZE*BOX_LIGHT_PROPORTION)
                                    ,BOX_SIZE, math.floor(BOX_SIZE*BOX_LIGHT_PROPORTION)))
        pygame.draw.rect(SCREEN, tuple(min(i+BOX_HIGHLIGHT_AMOUNT, 255) for i in color),
                         pygame.Rect(pos.x, pos.y, BOX_SIZE, math.floor(BOX_SIZE*BOX_LIGHT_PROPORTION)))

    @staticmethod
    def draw_bg():
        pygame.draw.rect(SCREEN, (255, 255, 255),
                         pygame.Rect(0, 0, SCREEN_SIZE.x, SCREEN_SIZE.y))
        pygame.draw.rect(SCREEN, (0, 0, 0),
                         pygame.Rect(BOARD_POS.x, BOARD_POS.y, 10 * BOX_SIZE,
                         20 * BOX_SIZE))
    @staticmethod
    def draw_text(pos, size, text):
        font = pygame.font.Font('pixel.ttf', size)
        text = font.render(text, True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (pos.x, pos.y)
        SCREEN.blit(text, textRect)
    
    @staticmethod
    def draw_gameover():
        pygame.draw.rect(SCREEN, (0, 0, 0),
                         pygame.Rect(0, 0, SCREEN_SIZE.x, SCREEN_SIZE.y))
        for i in range(len(GAME_SCREEN)):
            for j in range(len(GAME_SCREEN[i])):
                if GAME_SCREEN[i][j] == 'X':
                    drawing_manager.draw_box(vec(j, i).mult(BOX_SIZE).add(GAME_OFFSET)
                                            ,(200, 200, 200))
        for i in range(len(OVER_SCREEN)):
            for j in range(len(OVER_SCREEN[i])):
                if OVER_SCREEN[i][j] == 'X':
                    drawing_manager.draw_box(vec(j, i).mult(BOX_SIZE).add(OVER_OFFSET)
                                            ,(200, 200, 200))

################################
# CONSTANTS
################################

BOX_SIZE = 15
BOARD_POS = vec(150, 50)
SCREEN_SIZE = vec(500, 500)
SCREEN = pygame.display.set_mode([SCREEN_SIZE.x, SCREEN_SIZE.y])
GRAVITY = 2.0
PRE_DAS_DELAY = 0.3
DAS = 10.0
LEVEL_THRESHHOLD = 10
CLEAR_LINE_WAIT = 1 / GRAVITY
LINES_REWARD = {
    0: 0,
    1: 1,
    2: 3,
    3: 7,
    4: 20
}
COLORS = {
    "blue" : (0, 0, 255),
    "green" : (0, 255, 0),
    "red" : (255, 0, 0),
    "orange": (255, 153, 0),
    "aqua": (0, 255, 255),
    "purple": (153, 0, 255),
    "yellow": (255, 255, 0)
}
BOX_LIGHT_PROPORTION = 0.15
BOX_HIGHLIGHT_AMOUNT = 200
BOX_SHADOW_AMOUNT = -80
# FAST_MULTIPLIER cannot be one
FAST_MULTIPLIER = 3.0
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
J_PIECE = ([["..X.", "..X.", ".XX.", "...."], ["....", "X...", "XXX.", "...."],
            [".XX.", ".X..", ".X..", "...."], ["....", ".XXX", "...X", "...."]], "yellow")
L_PIECE = ([[".X..", ".X..", ".XX.", "...."], ["....", "XXX.", "X...", "...."],
            [".XX.", "..X.", "..X.", "...."], ["....", "...X", ".XXX", "...."]], "purple")
PIECES = [O_PIECE, T_PIECE, I_PIECE, Z_PIECE, S_PIECE, J_PIECE, L_PIECE]
GAME_OFFSET = vec((500 - 23 * BOX_SIZE) // 2, 100)
GAME_SCREEN = [".XXX...XXX..X...X.XXXXX",
               "X.....X...X.XX.XX.X....",
               "X.XXX.XXXXX.X.X.X.XXXXX",
               "X...X.X...X.X...X.X....",
               ".XXX..X...X.X...X.XXXXX"]
OVER_OFFSET = GAME_OFFSET.add(vec(0, BOX_SIZE*6))
OVER_SCREEN = [".XXX..X...X.XXXXX.XXXX.",
               "X...X.X...X.X.....X...X",
               "X...X..X.X..XXXXX.XXXX.",
               "X...X..X.X..X.....X..X.",
               ".XXX....X...XXXXX.X...X"]

################################
# GAME CLASSES
################################

class piece:
    def __init__(self, piece_info):
        self.states = piece_info[0]
        # Some pieces begin at the first row and other at the second
        # so with this if we ensure that the pieces begin at the very top
        self.pos = vec(3, 0 if "X" in self.states[0][0] else -1)
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
        for i in reversed(range(0, line+1)):
            if i == 0:
                dead_pieces.data[i] = [""] * 10
                continue
            for j in range(10):
                dead_pieces.data[i][j] = dead_pieces.data[i - 1][j]
    
    @staticmethod
    def clear_lines():
        amount = 0
        for i in range(20):
            full = True
            for j in range(10):      
                if dead_pieces.data[i][j] == "":
                    full = False
                    break
            if full:
                amount += 1
                dead_pieces.clear_line(i)
        return amount

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
    gravity_ts = 0
    das_ts = 0
    about_to_settle = False
    moving = 0
    running = True
    dead = False
    lines = 0
    level = 0
    score = 0

    @staticmethod
    def can_move(pos, state):
        for i in range(4):
            for j in range(4):
                if state[i][j] == "X":
                    if pos.x+j < 0:
                        return False
                    if pos.x+j >= 10:
                        return False
                    if pos.y+i >= 20:
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
    def das():
        # We do the down input here because it's convenient
        # since we call this every frame
        game.fast = pygame.key.get_pressed()[pygame.K_DOWN]
        if (game.moving == -1) and (time.time() > game.das_ts):
            if game.can_move(game.player_piece.pos.add(vec(-1, 0))
              ,game.player_piece.get_state()):
                game.player_piece.pos.x += -1
                game.das_ts = time.time() + 1.0 / DAS
        elif (game.moving == 1) and (time.time() > game.das_ts):
            if game.can_move(game.player_piece.pos.add(vec(1, 0))
              ,game.player_piece.get_state()):
                game.player_piece.pos.x += 1
                game.das_ts = time.time() + 1.0 / DAS

    @staticmethod
    def try_spawn_piece():
        p = piece(random.choice(PIECES))
        for i in range(4):
            if not(dead_pieces.colliding(p.pos, p.get_state(i))):
                dead_pieces.add_piece(game.player_piece.pos.add(vec(0, 1))
                                     ,game.player_piece.get_state(i)
                                     ,game.player_piece.color)
                game.score += (game.level + 1) * 10
                return (True, p)
        return (False, None)
    
    @staticmethod
    def frame():
        if game.dead:
            drawing_manager.draw_gameover()
            return
        drawing_manager.draw_bg()
        dead_pieces.draw()
        lines_removed = dead_pieces.clear_lines()
        game.lines += lines_removed
        game.score += (game.level + 1) * 100 * LINES_REWARD[lines_removed]
        if game.lines//LEVEL_THRESHHOLD > game.level:
            game.level += 1
            global GRAVITY
            GRAVITY += 1
        game.das()
        game.player_piece.draw()
        if time.time() > (game.gravity_ts - 
                         (((FAST_MULTIPLIER-1) / (FAST_MULTIPLIER*GRAVITY)
                         if game.fast else 0))):
            if game.can_move(game.player_piece.pos.add(vec(0, 1))
                              ,game.player_piece.get_state()):
                game.player_piece.pos.y += 1
                game.about_to_settle = False
            else:
                if game.about_to_settle:
                    game.about_to_settle = False
                    spawn_result = game.try_spawn_piece()
                    if spawn_result[0]:
                        game.player_piece = spawn_result[1]
                    else:
                        game.dead = True
                else:
                    game.about_to_settle = True
            game.gravity_ts = time.time() + 1 / GRAVITY
        drawing_manager.draw_text(vec(360, 70), 20, "SCORE")
        drawing_manager.draw_text(vec(360, 90), 20, "{:06d}".format(game.score))
        drawing_manager.draw_text(vec(360, 130), 20, "LEVEL")
        drawing_manager.draw_text(vec(360, 150), 20, "{:02d}".format(game.level))
        drawing_manager.draw_text(vec(360, 180), 20, "LINES")
        drawing_manager.draw_text(vec(360, 210), 20, "{:02d}".format(game.lines))

    @staticmethod
    def event_handler():
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game.try_rotate(True)
                    elif event.key == pygame.K_LCTRL:
                        game.try_rotate(False)
                    elif event.key == pygame.K_RIGHT:
                        if game.can_move(game.player_piece.pos.add(vec(1, 0))
                          ,game.player_piece.get_state()):
                            game.player_piece.pos.x += 1
                            game.moving = 1
                            game.das_ts = time.time() + PRE_DAS_DELAY
                    elif event.key == pygame.K_LEFT:
                        if game.can_move(game.player_piece.pos.add(vec(-1, 0))
                          ,game.player_piece.get_state()):
                            game.player_piece.pos.x += -1
                            game.moving = -1
                            game.das_ts = time.time() + PRE_DAS_DELAY
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                        game.moving = 0
    
    @staticmethod
    def start():
        pygame.init()
        pygame.display.set_caption("Pytris Reloaded")
        game.player_piece = piece(random.choice(PIECES))
        dead_pieces.init()
        game.gravity_ts = time.time() + 1 / GRAVITY
        while game.running:
            game.event_handler()
            game.frame()
            pygame.display.flip()
        pygame.quit()

game.start()
