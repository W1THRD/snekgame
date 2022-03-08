import warnings, sys, time, random, pickle
warnings.filterwarnings("ignore")
file = sys.argv[0]
import pgzrun



WIDTH = 660
HEIGHT = 600
TITLE = "SnekGame"
size = 20

def split(word):
    return [char for char in word]

def saveMap(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
def loadMap(filename):
    with open(filename, 'rb') as inp:
        l = pickle.load(inp)
        return l
        

class Wall:
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data
    def Draw(self):
        self.box = Rect((self.x * size, self.y * size), (size, size))
        if(self.data == 1):
            screen.draw.filled_rect( self.box, "grey" )

class Row:
    def __init__(self, y):
        self.l = []
        self.y = y
        for x in range(33):
            self.l.append(Wall(x, y, 0))
    def Draw(self):
        for x in range(33):
            self.l[x].Draw()
    def SetWall(self, x, data):
        self.l[x].data = data
        
class Level:
    def __init__(self, spawnX, spawnY, spawnD):
        self.l = []
        self.sx = spawnX
        self.sy = spawnY
        self.sd = spawnD
        for y in range(30):
            self.l.append(Row(y))
    def Draw(self):
        for y in range(30):
            self.l[y].Draw()
    def SetWall(self, x, y, data):
        self.l[y].SetWall(x, data)
    def GetWall(self, x, y):
        scan = self.l[int(y / size)].l[int(x / size)]
        return scan
        
    
class Food:
    def __init__(self):
        self.Respawn(0, 0)
    def Draw(self):
        screen.draw.filled_circle((self.x + size / 2, self.y + size / 2), (size / 2), "orange")
    def On(self, x, y):
        return self.x == x and self.y == y
    def Respawn(self, x, y):
        i = 0
        while i == 0:
            randomChoicesX = WIDTH/size
            self.x = random.randrange(0, randomChoicesX) * size
            randomChoicesY = HEIGHT/size
            self.y = random.randrange(0, randomChoicesY) * size
            if(level.GetWall(self.x, self.y).data == 1):
                i = 0
            else:
                i = 1
                
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
        self.sx = level.sx
        self.sy = level.sy
        self.sd = level.sd
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
        if(level.GetWall(self.links[0].x, self.links[0].y).data == 1):
            self.Rebirth()
        
                
    def Grow(self):
        
        last = self.links[len(self.links)-1]
        x = last.x
        y = last.y
        d = last.d
        if d == keys.LEFT:
            l = Link(x + size, y, d)
            
        elif d == keys.RIGHT:
            l = Link(x - size, y, d)
            
        elif d == keys.UP:
            l = Link(x, y + size, d)
            
        elif d == keys.DOWN:
            l = Link(x, y - size, d)
        self.links.append(l)
    def DGrow(self):
        
        last = self.links[len(self.links)-1]
        x = last.x
        y = last.y
        d = self.sd
        
        if d == keys.LEFT:
            l = Link(x + size, y, d)
            
        elif d == keys.RIGHT:
            l = Link(x - size, y, d)
            
        elif d == keys.UP:
            l = Link(x, y + size, d)
            
        elif d == keys.DOWN:
            l = Link(x, y - size, d)
        self.links.append(l)
            
            
        
    def Rebirth(self):
        self.ready = 2
        sounds.ouch.play()
        time.sleep(0.1)
        x = self.sx
        y = self.sy
        d = self.sd
        l = Link(x, y, d)
        self.links = [l]
        for i in range(3):
            self.DGrow()
        
#level = Level(200, 200, keys.RIGHT)
#level.SetWall(10, 7, 1)
level = loadMap('saves/random.snek')
snek = Snek(200, 200, keys.RIGHT)


for i in range(3):
    snek.Grow()
    
food = Food()



 
def update():
    if snek.ready == 1:
        snek.Update()
    
def draw():
    screen.clear()
    screen.fill((0, 128, 0))
    snek.Draw()
    food.Draw()
    level.Draw()
    if snek.ready == 1:
        text = str(len(snek.links)-4)
        screen.draw.text(text, (50, 30), color="orange", fontsize=32)
    elif snek.ready == 2:
        text = "Press SPACE to try again"
        screen.draw.text(text, (50, 30), color="orange", fontsize=32)
    elif snek.ready == 0:
        text = "Press SPACE to start"
        screen.draw.text(text, (50, 30), color="orange", fontsize=32)
       
        
    
    
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