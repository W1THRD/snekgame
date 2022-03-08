import warnings, sys, time, random
warnings.filterwarnings("ignore")

import pgzrun



WIDTH = 660
HEIGHT = 600
TITLE = "SnekGame"
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
    def __init__(self, x, y, d):
        self.x = x
        self.y = y
        self.d = d

class Snek:
    def __init__(self, x, y, d):
        l = Link(x, y, d)
        self.links = [l]
        self.ready = 0
        
    def Draw(self):
        for i in range(len(self.links)):
            BOX = Rect( (self.links[i].x, self.links[i].y), (size, size) )
            if i == 0:
                screen.draw.filled_rect( BOX, "gold" )
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
        
    def Update(self):
        
        for i in range(len(self.links)):
            if self.links[i].d == keys.LEFT:
                self.links[i].x -= size
            if self.links[i].d == keys.RIGHT:
                self.links[i].x += size
            if self.links[i].d == keys.UP:
                self.links[i].y -= size
            if self.links[i].d == keys.DOWN:
                self.links[i].y += size
        time.sleep(0.1)
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
            
    def Grow(self):
        
        last = self.links[len(self.links)-1]
        x = last.x
        y = last.y
        d = last.d
        if d == keys.LEFT:
            l = Link(x + size, y, d)
        if d == keys.RIGHT:
            l = Link(x - size, y, d)
        if d == keys.UP:
            l = Link(x, y + size, d)
        if d == keys.DOWN:
            l = Link(x ,y - size, d)
        self.links.append(l)
    def Rebirth(self):
        self.ready = 2
        sounds.ouch.play()
        randomChoicesX = WIDTH/size
        x = (random.randrange(0, randomChoicesX//2)+randomChoicesX//4) * size
        randomChoicesY = HEIGHT/size
        y = (random.randrange(0, randomChoicesY//2)+randomChoicesY//4) * size
        r = random.randrange(0, 3)
        if r == 0:
            d = keys.LEFT
        elif r == 1:
            d = keys.RIGHT
        elif r == 2:
            d = keys.UP
        elif r == 3:
            d = keys.DOWN
        l = Link(x, y, d)
        self.links = [l]
        for i in range(3):
            self.Grow()
        
        
snek = Snek(200, 200, keys.RIGHT)

for i in range(3):
    snek.Grow()
    
food = Food()


def draw():
    screen.clear()
    screen.fill((0, 128, 0))
    snek.Draw()
    food.Draw()
    
    if snek.ready == 1:
        text = str(len(snek.links)-4)
        screen.draw.text(text, (50, 30), color="orange", fontsize=32)
    elif snek.ready == 2:
        text = "Press SPACE to try again"
        screen.draw.text(text, (50, 30), color="orange", fontsize=32)
    elif snek.ready == 0:
        text = "Press SPACE to start"
        screen.draw.text(text, (50, 30), color="orange", fontsize=32)
    
def update():
    if snek.ready == 1:
        snek.Update()
    
    
def on_key_down(key):
    if snek.ready != 1 and key == keys.SPACE:
        snek.ready = 1
    if key == keys.LEFT and snek.links[0].d != keys.RIGHT:
        snek.links[0].d = key
    if key == keys.RIGHT and snek.links[0].d != keys.LEFT:
        snek.links[0].d = key
    if key == keys.UP and snek.links[0].d != keys.DOWN:
        snek.links[0].d = key
    if key == keys.DOWN and snek.links[0].d != keys.UP:
        snek.links[0].d = key

pgzrun.go()   