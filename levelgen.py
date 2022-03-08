import warnings, sys, time, random, pickle, pygame
warnings.filterwarnings("ignore")
file = sys.argv[0]

class keys:
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT


WIDTH = 660
HEIGHT = 600
TITLE = "Snek Game"
size = 20

def saveMap(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
def loadMap(filename):
    with open(filename, 'rb') as inp:
        l = pickle.load(inp)
        return l.value
        

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
            
        
            
level = Level(200, 200, keys.RIGHT)

for i in range(20):
    level.SetWall(random.randrange(1, WIDTH/size), random.randrange(1, HEIGHT/size), 1)
saveMap(level, 'saves/random.snek')

