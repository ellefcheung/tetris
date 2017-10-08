## tetris_empty.py
## Elle and Victoria
## collab: Ho Jung, Naomi, Evelyn, Christine, Elaine


from graphics import *
from random import *

####################
##  BLOCK CLASS
####################

class Block(Rectangle):

    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 3
    
    def __init__(self, point, color):
        self.x = point.getX()
        self.y = point.getY()
        self.color = color

        p1 = Point(self.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   self.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color_rgb(100, 100, 100)) # dark grey
        self.setOutline(color)
        self.setWidth(6)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        Rectangle.move(self,Block.BLOCK_SIZE*dx,Block.BLOCK_SIZE*dy)

    def can_move(self, board, dx, dy):
        if board.can_move(self.x + dx, self.y + dy):
            return True
        else:
            return False

####################
##  SHAPE CLASS
####################

class Shape(object):
    def __init__(self, coords, color):
        self.color = color
        self.block_list = []
        self.rotation_dir = 1
        self.shift_rotation_dir = False
        for pos in coords:
            self.block_list.append(Block(pos, color))

    def draw(self, win):
        for block in self.block_list:
            block.draw(win)

    def move(self, dx, dy):
        for i in range(4):
            self.block_list[i].move(dx,dy)

    def get_blocks(self):
        return self.block_list

    def can_move(self, board, dx, dy):
        for block in self.block_list:
            if block.can_move(board, dx, dy):
                result = True
            else:
                return False
        return result
            
    def can_rotate(self, board):
        for block in self.block_list:
            x = self.center_block.x - self.rotation_dir*self.center_block.y + self.rotation_dir*block.y
            y = self.center_block.y + self.rotation_dir*self.center_block.x - self.rotation_dir*block.x
            if block.can_move(board, x - block.x, y - block.y):
                result = True
            else:
                return False
        return result

    def rotate(self, board):
        #rotates shape in direction specified by rotation_dir
        for block in self.block_list:
            x = self.center_block.x - self.rotation_dir*self.center_block.y + self.rotation_dir*block.y
            y = self.center_block.y + self.rotation_dir*self.center_block.x - self.rotation_dir*block.x
            block.move(x - block.x, y - block.y)
        if self.shift_rotation_dir:
            self.rotation_dir = -1 * self.rotation_dir

####################
## SHAPE TYPES CLASS
####################
4
class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 2, center.y),
            Point(center.x - 1, center.y),
            Point(center.x    , center.y),
            Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, color_rgb(255, 200, 200)) # pink
        self.center_block = self.block_list[1]
        self.rotation_dir = -1
        self.shift_rotation_dir = True

class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, color_rgb(255, 225, 200)) # orange
        self.center_block = self.block_list[1]

            
class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y + 1),
                  Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self,coords, color_rgb(255, 255, 200)) # yellow
        self.center_block = self.block_list[2]

class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y + 1),
                  Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x, center.y + 1)]
        Shape.__init__(self,coords, color_rgb(215, 255, 215)) # green
        self.center_block = self.block_list[2]

    def rotate(self, board):
        return
        
class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y + 1),
                  Point(center.x, center.y + 1),
                  Point(center.x, center.y),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self,coords, color_rgb(200, 255, 255)) # blue
        self.center_block = self.block_list[2]
        self.shift_rotation_dir = True
        
class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x, center.y + 1)]
        Shape.__init__(self,coords, color_rgb(225, 200, 255)) # purple
        self.center_block = self.block_list[1]
        
class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x, center.y + 1),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self,coords, color_rgb(225, 225, 225)) # light grey
        self.center_block = self.block_list[1]
        self.shift_rotation_dir = True

####################
##  SCOREBOARD CLASS
####################

class ScoreBoard(object):

    def __init__(self, win, width):
        self.canvas = CanvasFrame(win, width * Block.BLOCK_SIZE,
                                  60)
        self.canvas.setBackground(color_rgb(100, 100, 100)) # dark grey
        self.score = 0
        self.score_point = Point(150, 15)
        self.score_text = Text(self.score_point, "score: 0")
        self.prettify(self.score_text)
        self.lvl = 0
        self.lvl_point = Point(150, 45)
        self.lvl_text = Text(self.lvl_point, "level: 1")
        self.prettify(self.lvl_text)

    def prettify(self, text):
        text.setOutline(color_rgb(255, 255, 255))
        text.draw(self.canvas)

    def update_score(self):
        self.score_text.undraw()
        self.score_text = Text(self.score_point, "score: " + str(self.score))
        self.prettify(self.score_text)

    def update_lvl(self):
        print self.score % 1000
        if self.score % 1000 == 0:
            self.lvl_text.undraw()
            self.lvl = self.lvl + 1
            self.lvl_text = Text(self.lvl_point, "level: " + str(self.lvl))
            self.prettify(self.lvl_text)
                                                

####################
##  BOARD CLASS
####################

class Board(object):

    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.win = win

        self.scoreboard = ScoreBoard(self.win, self.width)
        self.rows_completed = 0

        self.canvas = CanvasFrame(self.win, self.width * Block.BLOCK_SIZE,
                                  self.height * Block.BLOCK_SIZE)

        self.canvas.setBackground(color_rgb(150, 150, 150)) # dark ish grey
        self.grid = {} # (x, y): Block object
        
        self.line_list = []
        self.make_grid()
        self.draw_grid()
        
        self.game_over_list = []
        self.pause_list = []

    def update_scoreboard(self):
        self.scoreboard.score = self.rows_completed * 100
        self.scoreboard.update_score()
        self.scoreboard.update_lvl()
        
    def make_grid(self):
        for x in range(10):
            line = Line(Point(30*x + Block.OUTLINE_WIDTH, 0), Point(30*x + Block.OUTLINE_WIDTH, 600))
            line.setWidth(6)
            line.setFill(color_rgb(155, 155, 155))
            self.line_list.append(line)
        for y in range(20):
            line = Line(Point(0, 30*y + Block.OUTLINE_WIDTH), Point(300, 30*y + Block.OUTLINE_WIDTH))
            line.setWidth(6)
            line.setFill(color_rgb(155, 155, 155))
            self.line_list.append(line)

    def draw_grid(self):
        for line in self.line_list:
            line.draw(self.canvas)

    def undraw_grid(self):
        for line in self.line_list:
            line.undraw()

    def draw_shape(self, shape):
        #draws a shape on the board if there is space for it
        #returns True if there is space, otherwise returns False
        #check to see if shape can be drawn at current location
        #if shape.can_move(self.canvas, 0, 0):

        if self.can_move(0, 0) == True:
            shape.draw(self.canvas)
            return True
        else:
            return False

    def can_move(self, x, y):
        # is position on board
        if 0<= x <=9 and 0 <= y <= 19:
            result = True
        else:
            return False
        #is the position already occupied
        if (x, y) in self.grid:
            return False
        return result

    def add_shape(self, shape):
        #add a shape to the grid (the blocks) using x,y coords as the key
        #use get_blocks method on shape to get block list
        for block in shape.block_list:
            self.grid[(block.x, block.y)] = block

    def delete_row(self, y):
        #delete all the blocks in row y from the grid
        #erase them from the canvas
        if self.is_row_complete(y):
            for x in range(0, 10):
                block = self.grid[(x, y)]
                block.undraw()
                del self.grid[(x, y)]
            

    def is_row_complete(self, y):
        #checks if all squares in row y are occupied
        #returns bool
        for x in range(0, 10):
            if (x, y) in self.grid:
                result = True
            else:
                return False
        return result
        

    def move_down_rows(self,y_start):
        #move all blocks in each row starting at y start and up, down 1 square
        #update grid
        for y in range(y_start, 0, -1):
            for x in range(0, 10):
                if (x, y) in self.grid:
                    block = self.grid[(x, y)]
                    del self.grid[(x, y)]
                    block.move(0, 1)
                    self.grid[(block.x, block.y)] = block
                

    def remove_complete_rows(self):
        # remove all complete rows
        # move rows above down
        for y in range(0,20):
            if self.is_row_complete(y):
                self.delete_row(y)
                self.move_down_rows(y-1)
                self.rows_completed = self.rows_completed + 1
                self.update_scoreboard()
                

    def game_over(self):
        for block in self.grid.values():
            block.setOutline(color_rgb(150, 150, 150))
        self.undraw_grid()

        n = 75 + Block.OUTLINE_WIDTH
        for char in "GAME":
            n = n + 30
            character = Text(Point(n, 138), str(char))
            self.game_over_list.append(character)
        n = 75 + Block.OUTLINE_WIDTH
        for char in "OVER":
            n = n + 30
            character = Text(Point(n, 168), str(char))
            self.game_over_list.append(character)
        for character in self.game_over_list:
            character.setOutline(color_rgb(255, 255, 255))
            character.draw(self.canvas)

    def pause(self):
        n = 45 + Block.OUTLINE_WIDTH
        for char in "PAUSED":
            n = n + 30
            character = Text(Point(n, 168), str(char))
            self.pause_list.append(character)
        for character in self.pause_list:
            character.setOutline(color_rgb(255, 255, 255))
            character.draw(self.canvas)

    def unpause(self):
        for character in self.pause_list:
            character.undraw()



######################
##  WTPTETRIS CLASS###
######################

class WTPTetris(object):
    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    x = 0
    DIRECTION = {'Left':(-1,0), 'Right':(1,0), 'Down':(0,1), 'space':(0,20), 'p':(0,0), 'P':(0,0)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20

    def __init__ (self, win):
        self.is_game_over = False
        self.is_paused = False

        self.board = Board (win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        
        self.win = win
        self.delay = 1000
        self.key = self.win.bind_all('<Key>', self.key_pressed)
        self.current_shape = self.create_new_shape()
        self.animate_shape()

        
        

        #draw current_shape on the board using methods from BOard class
        #animate the shape

    def animate_shape(self):
        #move shape down at equal intervals specified by delay instance variable
        if not self.is_paused:
            self.do_move("Down")
        self.win.after(self.delay, self.animate_shape)

    def create_new_shape(self):
        #creates random new shape centered at top of board
        #return the shape
        shape = WTPTetris.SHAPES[randint(0, 6)]
        shape = shape(Point(5, 0))
        for block in shape.block_list:
            if (block.x, block.y) in self.board.grid:
                return False
        self.board.draw_shape(shape)
        return shape

    def do_move (self, direction):
        #move current shape in direction specified by parameter
        #check if space CAN move, if True, move it and return True
        #if it can't and the direction tried was Down, add the current shape to the board
        #remove the completed rows if nay
        #create a new random shape, set current shape attribute
        #if shape cannot be drawn on the board, display game over
        #return False
        if self.is_game_over:
            return False
        dx = self.DIRECTION[direction][0]
        dy = self.DIRECTION[direction][1]
        if self.current_shape.can_move(self.board, dx, dy):
            self.current_shape.move(dx, dy)
            return True
        if direction == "Down":
            self.board.add_shape(self.current_shape)
            self.board.remove_complete_rows()
            n = self.create_new_shape()
            if n == False:
                self.board.game_over()
                self.is_game_over = True
            else:
                self.current_shape = n
        else:
            return False

    def do_rotate(self):
        #if current shape can be rotated, rotate
        if self.current_shape.can_rotate(self.board):
            self.current_shape.rotate(self.board)

    def key_pressed(self, event):

        #modify function so that arrow keys cause directional moves in said direction
        #if user presses space bar, the shape will keep moving down until it can't go further
        #if user pressed UP the shape rotates
        #if user presses 'P' or 'p' game pauses
        key = event.keysym
        
        if not self.is_game_over:
            if key == 'P' or key == 'p':
                self.is_paused = not self.is_paused
                if self.is_paused:
                    self.board.pause()
                else:
                    self.board.unpause()
            if not self.is_paused:
                if key == 'Up':
                    self.do_rotate()
                elif key == 'space':
                    while self.do_move("Down"):
                        pass
                else:
                    self.do_move(key)

####################
##  START GAME
####################

        
win = Window("WTP Tetris")

game = WTPTetris(win)

win.mainloop()
