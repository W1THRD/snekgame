import warnings, sys, time, random
warnings.filterwarnings("ignore")

import pgzrun



WIDTH = 660
HEIGHT = 600
TITLE = "Snek Game"
size = 20

class Food:
    def __init__(self):
        self.Respawn(0, 0)
    def Draw(self):
        screen.draw.filled_circle((self.x + size / 2, self.y + size / 2), (size / 2), "orange")
    def On(self, x, y):
        return self.x == x and self.y == y
    def Respawn(self, x, y):
        randomChoicesX = WIDTH/size
        self.x = random.randrange(0, randomChoicesX) * size
        randomChoicesY = HEIGHT/size
        self.y = random.randrange(0, randomChoicesY) * size
        print("Food is at " + str(self.x) + ", " + str(self.y))


class Link:
    def __init__(self, x, y, d, c):
        self.x = x
        self.y = y
        self.d = d
        self.c = c

class Snek:
    def __init__(self, x, y, d, c, r):
        l = Link(x, y, d, c)
        self.links = [l]
        self.ready = r
        
    def Draw(self):
        for i in range(len(self.links)):
            BOX = Rect( (self.links[i].x, self.links[i].y), (size, size) )
            if i == 0:
                screen.draw.filled_rect( BOX, self.links[0].c )
            else:
                screen.draw.filled_rect( BOX, "green" )
            
    def Offscreen(self):
        if self.links[0].x < 0 or self.links[0].x >= WIDTH or self.links[0].y < 0 or self.links[0].y >= HEIGHT :
            return True
        else:
            return False
    def On(self, x, y):
        for i in range(1, len(self.links)):
            if self.links[i].x == x and self.links[i].y == y:
                return True
        return False
    def OnBody(self, x, y):
        for i in range(0, len(self.links)):
            if self.links[i].x == x and self.links[i].y == y:
                return True
        return False
        
    def Update(self, other):
        
        for i in range(len(self.links)):
            if self.links[i].d == keys.LEFT or self.links[i].d == keys.A :
                self.links[i].x -= size
            if self.links[i].d == keys.RIGHT or self.links[i].d == keys.D :
                self.links[i].x += size
            if self.links[i].d == keys.UP or self.links[i].d == keys.W :
                self.links[i].y -= size
            if self.links[i].d == keys.DOWN or self.links[i].d == keys.S :
                self.links[i].y += size
        
        for i in range(len(self.links)-1, 0, -1):
            self.links[i].d = self.links[i-1].d
        if food.On(self.links[0].x, self.links[0].y):
            sounds.nom.play()
            self.Grow()
            #self.Rebirth()
            food.Respawn(self.links[0].x, self.links[0].y)
        if(self.Offscreen()):
            self.Rebirth()
        if(self.On(self.links[0].x, self.links[0].y)):
            self.Rebirth()
            food.Respawn(self.links[0].x, self.links[0].y)
        if(other.OnBody(self.links[0].x, self.links[0].y)):
            self.Rebirth()
            food.Respawn(self.links[0].x, self.links[0].y)
        
            
    def Grow(self):
        
        last = self.links[len(self.links)-1]
        x = last.x
        y = last.y
        d = last.d
        c = "green"
        if d == keys.LEFT or d == keys.A :
            l = Link(x + size, y, d, c)
        if d == keys.RIGHT or d == keys.D:
            l = Link(x - size, y, d, c)
        if d == keys.UP or d == keys.W:
            l = Link(x, y + size, d, c)
        if d == keys.DOWN or d == keys.S:
            l = Link(x ,y - size, d, c)
        self.links.append(l)
    def Rebirth(self):
        self.ready = 2
        sounds.ouch.play()
        randomChoicesX = WIDTH/size
        x = (random.randrange(0, randomChoicesX//2)+randomChoicesX//4) * size
        randomChoicesY = HEIGHT/size
        y = (random.randrange(0, randomChoicesY//2)+randomChoicesY//4) * size
        r = random.randrange(0, 3)
        c = self.links[0].c
        if r == 0:
            d = keys.LEFT
        elif r == 1:
            d = keys.RIGHT
        elif r == 2:
            d = keys.UP
        elif r == 3:
            d = keys.DOWN
        l = Link(x, y, d, c)
        self.links = [l]
        for i in range(3):
            self.Grow()
        
        
snek1 = Snek(200, 200, keys.RIGHT, "gold", 0)
snek2 = Snek(400, 400, keys.LEFT, "red", 0)

for i in range(3):
    snek1.Grow()
    snek2.Grow()
    
food = Food()


def draw():
    screen.clear()
    screen.fill((0, 128, 0))
    snek1.Draw()
    snek2.Draw()
    food.Draw()
    # Player 1 text
    if snek1.ready == 1:
        text = "P1: " + str(len(snek1.links)-4)
        screen.draw.text(text, (50, 30), color="orange", fontsize=32)
    elif snek1.ready == 2:
        text = "P1: Press Z to try again"
        screen.draw.text(text, (50, 30), color="orange", fontsize=32)
    elif snek1.ready == 0:
        text = "P1: Press Z to start"
        screen.draw.text(text, (50, 30), color="orange", fontsize=32)
        
    # Player 2 text
    if snek2.ready == 1:
        text = "P2: " + str(len(snek2.links)-4)
        screen.draw.text(text, (50, 50), color="red", fontsize=32)
    elif snek2.ready == 2:
        text = "P2: Press X to try again"
        screen.draw.text(text, (50, 50), color="red", fontsize=32)
    elif snek2.ready == 0:
        text = "P2: Press X to start"
        screen.draw.text(text, (50, 50), color="red", fontsize=32)
    
def update():
    if snek1.ready == 1:
        snek1.Update(snek2)
    if snek2.ready == 1:
        snek2.Update(snek1)
    time.sleep(0.1)
    
    
def on_key_down(key):
    # Player 1
    if snek1.ready != 1 and key == keys.Z:
        snek1.ready = 1
    if key == keys.LEFT and snek1.links[0].d != keys.RIGHT:
        snek1.links[0].d = key
    if key == keys.RIGHT and snek1.links[0].d != keys.LEFT:
        snek1.links[0].d = key
    if key == keys.UP and snek1.links[0].d != keys.DOWN:
        snek1.links[0].d = key
    if key == keys.DOWN and snek1.links[0].d != keys.UP:
        snek1.links[0].d = key
    # Player 2
    if snek2.ready != 1 and key == keys.X:
        snek2.ready = 1
    if key == keys.A and snek2.links[0].d != keys.D:
        snek2.links[0].d = key
    if key == keys.D and snek2.links[0].d != keys.A:
        snek2.links[0].d = key
    if key == keys.W and snek2.links[0].d != keys.S:
        snek2.links[0].d = key
    if key == keys.S and snek2.links[0].d != keys.W:
        snek2.links[0].d = key

pgzrun.go()   