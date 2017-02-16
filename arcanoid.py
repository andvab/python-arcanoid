from tkinter import *

WIDTH = 600
HEIGHT = 400

class Game:
    start = 0
    end   = 0
    point = 0
    score = 0
    
    def __init__(self):
        self.score = canvas.create_text(80, HEIGHT - 100,
                         text='SCORE: 0',
                         font="Arial 20",
                         fill="black")
                         
    def update_score(self):
        self.point += 1
        canvas.itemconfig(self.score, text='SCORE: ' + str(self.point))
        
    def loose_text(self):
        self.score = canvas.create_text(WIDTH / 2, HEIGHT / 2 + 10,
                         text='YOU LOOSE !',
                         font="Arial 20",
                         fill="black")
                         
    def win_text(self):
        self.score = canvas.create_text(WIDTH / 2, HEIGHT / 2 + 10,
                         text='YOU WIN !!!',
                         font="Arial 20",
                         fill="black")

class Desc:
    canv    = 0
    width   = 140
    height  = 20
    padding = 10
    
    def createDesc(self):
        x1 = 10
        x2 = x1 + self.width
        y1 = HEIGHT - 30
        y2 = y1 + self.height
        self.canv = canvas.create_rectangle(x1, y1, x2, y2,fill="white",outline="blue")
        
        ball.createBall(x1 + ((x2 - x1)/2 - ball.radius), y1 - ball.diameter)
        
    def moveDesc(self, pos_x, pos_y):
        x1 = 0
        y1 = HEIGHT - self.padding - self.height
        x2 = 0
        y2 = HEIGHT - self.padding
        
        if pos_x - (self.width / 2) > 0 and pos_x +(self.width / 2) < WIDTH:
            x1 = pos_x - (self.width / 2)
            x2 = pos_x + (self.width / 2)
        else:
            if pos_x - (self.width / 2) <= 0:
                x2 = self.width
            else:
                x1 = WIDTH - self.width
                x2 = WIDTH
                
        canvas.coords(self.canv, x1, y1, x2, y2)

        desc_x1, desc_y1, desc_x2, desc_y2 = canvas.coords(self.canv)

        ball_x1 = desc_x1 + (desc_x2 - desc_x1) / 2 - ball.radius
        ball_y1 = desc_y1 - ball.diameter
        ball_x2 = ball_x1 + ball.diameter
        ball_y2 = desc_y1

        if game.start == 0:
            canvas.coords(ball.canv, ball_x1, ball_y1, ball_x2, ball_y2)
            
    def getCoords(self):
        desc_x1, desc_y1, desc_x3, desc_y2 = canvas.coords(self.canv)
        desc_x2 = desc_x1 + self.width / 2
        
        return [desc_x1, desc_x2, desc_x3, desc_y1, desc_y2]

class Ball:
    moveX    = 1
    moveY    = 1
    canv     = 0
    diameter = 20
    radius   = diameter /2
    
    def createBall(self, x1, y1):
        x2 = x1 + self.diameter
        y2 = y1 + self.diameter
        self.canv = canvas.create_oval(x1, y1, x2, y2, fill="blue")
    
    def moveBall(self): 
        ball_x1, ball_y1, ball_x2, ball_y2 = canvas.coords(self.canv)
        ball_bottom_point = ball_x1 + self.radius
        
        desc_x1, desc_x2, desc_x3, desc_y1, desc_y2 = desc.getCoords()
        
        # desk
        if ball_bottom_point >= desc_x1 and ball_bottom_point <= desc_x3 and ball_y2 == desc_y1:
            if ball_bottom_point >= desc_x1 and ball_bottom_point < desc_x2 and self.moveX > 0:
                self.moveX = self.moveX * (-1)
                
            if ball_bottom_point >= desc_x2 and ball_bottom_point <= desc_x3 and self.moveX < 0:
                self.moveX = self.moveX * (-1)
                
            self.moveY = self.moveY * (-1)
        elif ball_y2 > HEIGHT:
            game.end = 1
            game.loose_text()
        
        #right wall
        if ball_x2 == WIDTH:
            self.moveX = self.moveX * (-1)
        #top wall
        if ball_y1 == 0:
            self.moveY = self.moveY * (-1)
        #left wall
        if ball_x1 == 0:
            self.moveX = self.moveX * (-1)
        
        #blocks
        i=0
        while i < len(blocks):
            block = blocks[i]
            hit   = 0
            ball_center_x = ball_x1 + self.radius
            ball_center_y = ball_y1 + self.radius
            
            #block_bottom_border
            if block.x1 <= ball_center_x < block.x2 and block.y2 == ball_y1:
                self.moveY = self.moveY * (-1)
                hit  = 1

            #block_bottom_top
            if block.x1 < ball_center_x <= block.x2 and block.y1 == ball_y2:
                self.moveY = self.moveY * (-1)
                hit  = 1

            #block_bottom_left
            if block.y1 <= ball_center_y < block.y2 and block.x1 == ball_x2:
                self.moveX = self.moveX * (-1)
                hit  = 1

            #block_bottom_right
            if (block.y1 - self.radius) < ball_center_y <= (block.y2 + self.radius) and block.x2 == ball_x1:
                self.moveX = self.moveX * (-1)
                hit  = 1
                
            if hit:
                game.update_score()
                block.strength -= 1
                canvas.itemconfig(block.canv, fill=block.color[block.strength])
                
                if block.strength == 0:
                    canvas.delete(block.canv)
                    blocks.remove(block)
                
                if len(blocks) == 0:
                    game.end = 1
                    game.win_text()
                    
                break
            
            i += 1
            
        canvas.move(self.canv, self.moveX, self.moveY)
        
        if game.end == 0:
            root.after(10, self.moveBall)
        
class Block:
    strength = 1
    color    = ['', 'yellow', 'green', 'red']
    width    = 100
    height   = 20
    canv     = 0
    x1       = 0
    y1       = 0
    x2       = 0
    y2       = 0
    
    def create(self, x1, y1, x2, y2):
        self.canv = canvas.create_rectangle(x1, y1, x2, y2, fill=self.color[self.strength])
        
    def build_block(self, count):
        x1 = 0
        y1 = 0
        
        for i in range (count):
            x2 = x1 + self.width
            
            if x2 > WIDTH:
                y1 = y1 + self.height
                x1 = 0
                x2 = x1 + self.width
                
            y2 = y1 + self.height
            
            self.create(x1, y1, x2, y2)
            
            x1 = x2
            
    def createBlock(self):
        self.x2 = float(self.x1 + self.width)
        self.y2 = float(self.y1 +  self.height)
        
        self.create(self.x1, self.y1, self.x2, self.y2)
    
def OnMouseEvent(event):
    getx  = event.x_root
    gety  = event.y_root
    pos_x = getx - root.winfo_rootx()
    pos_y = gety - root.winfo_rooty()
    
    desc.moveDesc(pos_x, pos_y)
    
       
def OnButton1Event(event):
    if game.start == 0:
        game.start = 1
        ball.moveBall()
        
def blocks(count):
    blocks = []
    
    x1 = 0
    y1 = 0

    for i in range (count):
        block = Block()
        block.x1 = x1
        block.y1 = y1
        
        if i < 12:
            block.strength = 3
        elif i < 24:
            block.strength = 2
        
        block.createBlock()
        
        blocks.append(block)
        
        x1 = block.x2
        
        if x1 + block.width > WIDTH:
            x1 = 0
            y1 = block.y2
        
    return blocks
    
root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)

canvas.pack()
root.update()
 
game = Game()
ball = Ball()
desc = Desc()
desc.createDesc()

blocks = blocks(30)

canvas.bind("<Motion>", OnMouseEvent)
canvas.bind("<Button-1>", OnButton1Event)

root.mainloop()
