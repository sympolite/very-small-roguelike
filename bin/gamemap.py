import tdl
import random
import gameobject

#each palette is a 4-tuple of RBG 3-tuples
#in order, these are DARK floor, DARK wall, LIGHT floor, LIGHT wall
palettes = {'grey': ((45, 45, 45), (0, 0, 0), (180, 180, 180), (90, 90, 90))}
MAXWIDTH = 9
MAXHEIGHT = 9
MINWIDTH = 3
MINHEIGHT = 3
FOV_ALGO = 'BASIC'
FOV_LIGHT_WALLS = True

#======================================================================================
#CLASSES
#======================================================================================


class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.explored = False
 
        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: 
            block_sight = blocked
        self.block_sight = block_sight


#======================================================================================

class Room:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.room_type = 1

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)


#===============================================================================


class GameMap:
    def __init__(self, width, height, palette, con):
        self.con = con
        self.width = width
        self.height = height
        self.dimensions = (width, height)
        self.size = height*width
        
        self.palette = palette
        self.rooms = []
        self.num_rooms = 0
        self.tilemap = self.create_walls()
        self.create_tilemap()       
        
        #for i in range(random.randint(1,10)):
        #    x = random.randint(0,self.width)
        #    y = random.randint(0,self.height)
        #    self.tilemap[x][y].blocked = True
        #    self.tilemap[x][y].block_sight = True
#======================================================================================================

    def in_map_bounds(self, x, y):
        if 0 < x < self.width-1 and 0 < y < self.height-1:
            return True
        return False

#======================================================================================================

    def create_tilemap(self):
        global MINWIDTH, MINHEIGHT, MAXWIDTH, MAXHEIGHT
        
        for x in range(0, random.randint(12, 24)):
            r = Room(random.randint(0, self.width-1),
                     random.randint(0, self.height-1),
                     random.randint(MINWIDTH, MAXWIDTH),
                     random.randint(MINHEIGHT, MAXHEIGHT))
            #print(str(x) + ": (" + str(r.x1) + ',' + str(r.y1) + '), (' + str(r.x2) + ',' + str(r.y2) + ')')

            self.create_room(r, random.randint(1, 5))
            (new_x, new_y) = r.center()
            if self.num_rooms > 0:
                (prev_x, prev_y) = self.rooms[self.num_rooms-1].center()
                self.create_tunnels(prev_x, prev_y, new_x, new_y, 1)
            self.rooms.append(r)
            self.num_rooms += 1
            
#===========================================================================================================
    def create_walls(self):
        return [[Tile(True) for y in range(self.height)] for x in range(self.width)]

#===========================================================================================================        
    def create_room(self, room, variance):
        if room.room_type == 1:
            for x in range(room.x1, room.x2):
                for y in range(room.y1, room.y2):
                    if self.in_map_bounds(x, y):
                        self.tilemap[x][y].blocked = False
                        self.tilemap[x][y].block_sight = False

        #elif room.room_type == 2:
            #self.create_elliptical_room(room)

        #else:
        #    for x in range(room.x1 + random.randint(-variance, variance),
        #                   room.x2 + random.randint(-variance, variance)):
        #        for y in range(room.y1 + random.randint(-variance, variance),
        #                       room.y2 + random.randint(-variance, variance)):
        #            if self.in_map_bounds(x, y):
        #                self.tilemap[x][y].blocked = False
        #                self.tilemap[x][y].block_sight = False

    #deprecated
    def create_elliptical_room(self, room):

        w = abs(room.x2 - room.x1)
        h = abs(room.y2 - room.y1)
        a = max(w, h)
        b = min(w, h)
        xc, yc = room.center()
        x = 0
        y = b
        a2 = a ** 2
        b2 = b ** 2
        crit1 = -(a2 / 4 + a % 2 + b2)
        crit2 = -(b2 / 4 + b % 2 + a2)
        crit3 = -(b2 / 4 + b % 2)
        t = -a2 * y
        dxt = 2 * b2 * x
        dyt = -2 * a2 * y
        d2xt = 2 * b2
        d2yt = 2 * a2
        width = 1

        def incx():
            nonlocal x, t, dxt, d2yt
            x += 1
            dxt += d2xt
            t += dxt

        def incy():
            nonlocal y, t, dyt, d2yt
            y -= 1
            dyt += d2yt
            t += dyt

        while y >= 0 and x <= a:
            if t + b2*x <= crit1 or t + a2*y <= crit3:
                incx()
                width += 2
            elif t - a2*y > crit2:
                for i in range(0, i):
                    if self.in_map_bounds(xc-x+ i, yc-y):
                        self.tilemap[xc-x + i][yc-y].blocked = False
                        self.tilemap[xc-x + i][yc-y].block_sight = False
                        print('filled: ' + str(xc-x+i) + ', ' + str(yc-y))
                if y != 0:
                    for i in range(0,width):
                        if self.in_map_bounds(xc - x + i, yc + y):
                            self.tilemap[xc - x + i][yc + y].blocked = False
                            self.tilemap[xc - x + i][yc + y].block_sight = False
                            print('filled: ' + str(xc - x + i) + ', ' + str(yc + y))
                incy()
            else:
                for i in range(0, width):
                    if self.in_map_bounds(xc - x + i, yc-y):
                        self.tilemap[xc-x+i][yc-y].blocked = False
                        self.tilemap[xc-x+i][yc-y].block_sight = False
                        print('filled: ' + str(xc - x + i) + ', ' + str(yc - y))
                if y != 0:
                    for i in range(0,width):
                        if self.in_map_bounds(xc - x + i, yc + y):
                            self.tilemap[xc - x + i][yc + y].blocked = False
                            self.tilemap[xc - x + i][yc + y].block_sight = False
                            print('filled: ' + str(xc - x + i) + ', ' + str(yc + y))
                incx()
                incy()
                width += 2
        if b == 0:
            for i in range(2*a+1):
                if self.in_map_bounds(xc - a, yc):
                    self.tilemap[xc - a + i][yc].blocked = False
                    self.tilemap[xc - a + i][yc].block_sight = False
                    print('filled: ' + str(xc - a + i) + ', ' + str(yc))
                    
#============================================================================================================                    
    def create_tunnels(self, start_x, start_y, end_x, end_y, width):
            if random.randint(0, 1):
                #first move horizontally, then vertically
                for i in range(1, width+1):
                    j = i - ((width//2)+1)
                    self.create_h_tunnel(start_x, end_x, start_y+j)
                    self.create_v_tunnel(start_y, end_y, end_x+j)
            else:
                #first move vertically, then horizontally
                for i in range(1, width+1):
                    j = i - ((width//2)+1)
                    self.create_v_tunnel(start_y, end_y, start_x+j)
                    self.create_h_tunnel(start_x, end_x, end_y+j)

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if not self.in_map_bounds(x, y):
                break
            self.tilemap[x][y].blocked = False
            self.tilemap[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if not self.in_map_bounds(x, y):
                break
            self.tilemap[x][y].blocked = False
            self.tilemap[x][y].block_sight = False
#=============================================================================================================

    def is_visible_tile(self, x, y):
        if self.in_map_bounds(x, y):
            if self.tilemap[x][y].blocked:
                return False
            elif self.tilemap[x][y].block_sight:
                return False
            else:
                return True
        else:
            return False
    """    
    def compute_fov(self, player):
        print('Computing Fov!')
        global recompute
        if recompute:
            recompute = False
            visible_tiles = 
            return visible_tiles
    """    
    def draw(self, player):
        visible_tiles = tdl.map.quick_fov(player.x, player.y,
                                         self.is_visible_tile,
                                         fov=FOV_ALGO,
                                         radius=player.sight,
                                         lightWalls=False)
        for y in range(self.height):
            for x in range(self.width):
                #self.compute_fov(player)
                visible = (x, y) in visible_tiles
                wall = self.tilemap[x][y].block_sight
                if not visible:
                    if self.tilemap[x][y].explored:
                        if wall:
                            self.con.draw_char(x, y, None, fg=None, bg=self.palette[1])
                        else:
                            self.con.draw_char(x, y, None, fg=None, bg=self.palette[0])        
                else:
                    if wall:
                        self.con.draw_char(x, y, None, fg=None, bg=self.palette[3])
                    else:
                        self.con.draw_char(x, y, None, fg=None, bg=self.palette[2])
                    self.tilemap[x][y].explored = True

    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.con.draw_char(x, y, ' ', fg=(0, 0, 0), bg=(0, 0, 0))
                    
        
if __name__ == "__main__":
    print("Please run game.py!")
