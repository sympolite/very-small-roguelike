import tdl
import sys

palettes = {'grey': ((45, 45, 45), (0, 0, 0), (180, 180, 180), (90, 90, 90))}
MAXWIDTH = 9
MAXHEIGHT = 9
MINWIDTH = 3
MINHEIGHT = 3
FOV_ALGO = 'BASIC'
FOV_LIGHT_WALLS = True


class Tile:
    # a tile of the map and its properties
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.explored = False

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


class GameMap:
    def __init__(self, map_id, con):
        self.map_id = str(map_id)
        self.con = con
        self.palette = palettes['grey']
        self.width, self.height = 0
        self.tilemap = []
        self.tilemap = [[]]
        self.load_tilemap()
        self.create_tilemap()

    def in_map_bounds(self, x, y):
        if 0 < x < self.width-1 and 0 < y < self.height-1:
            return True
        return False

    def load_tilemap(self):
        width = 0
        height = 0
        map_data = []
        try:
            with open('maps/'+self.map_id+'.map') as map_file:
                for counter, line in enumerate(map_file):
                    if 0 < len(line) <= MAXWIDTH and height <= MAXHEIGHT:
                        map_data.append(line)
                        self.height += 1
                        if counter == 0:
                            self.width = len(line)
                        elif len(line) != self.width:
                            raise ValueError
                        else:
                            pass
                    else:
                        raise ValueError
            for datum in map_data:
                for char in datum:
                    if char != "-" or char != "#":
                        raise ValueError
            self.create_tilemap(map_data)
        except IOError:
            print("ERROR - .map file not found")
            sys.exit(1)
        except ValueError:
            print("ERROR - Invalid map data")
            sys.exit(1)

    def create_tilemap(self, mapdata):
        for i, row in enumerate(mapdata):
            for j, column in enumerate(mapdata[i]):
                if column == '-':
                    self.tilemap[j][i] = Tile(False)
                elif column == '#':
                    self.tilemap[j][i] = Tile(True)
                else:
                    pass

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
