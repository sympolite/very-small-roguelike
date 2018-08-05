import tdl
import gamemap
from random import randint
import math
import messagebox

all_objects = []
con = None
msgbox = None
player = None
current_map = None


def initialize_for_all(_con, _msgbox):
    global con, msgbox
    con = _con
    msgbox = _msgbox


def set_player(_player):
    global player
    player = _player


def set_map(curmap):
    global current_map
    current_map = curmap
    #print(type(curmap))


class GameObject:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, char, color, blocks=True):
        global all_objects, con, msgbox, current_map
        self.player = player
        self.char = char
        self.color = color
        self.con = con
        self.current_map = current_map
        self.msgbox = msgbox
        self.x = 0
        self.y = 0
        self.blocks = blocks
        all_objects.append(self)
        #print(type(self.current_map))

    def get_distance(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            distance = 1
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return (dx, dy)

    def next_to_object(self, dx, dy):
        global all_objects
        for obj in all_objects:
            if obj.blocks and obj.x == self.x+dx and obj.y == self.y+dy:
                return True
        return False

    def spawn(self):
        while current_map.tilemap[self.x][self.y].blocked:
            self.x = randint(1,self.con.width-1)
            self.y = randint(1,self.con.height-1)
 
    def move(self, dx, dy):
        #move by the given amount
        if not current_map.tilemap[self.x + dx][self.y + dy].blocked and not self.next_to_object(dx, dy):
            self.x += dx
            self.y += dy
 
    def draw(self):
        #draw the character that represents this object at its position
        self.con.draw_char(self.x, self.y, self.char, self.color)
        #print('id of console for GameObject ' + str(id(self)) + ': ' + str(id(self.con)))
 
    def clear(self):
        #erase the character that represents this object
        self.con.draw_char(self.x, self.y, ' ', self.color, bg=None)


class Player(GameObject):
    def __init__(self, name, hp=100):
        GameObject.__init__(self, '@', (255, 0, 200))
        self.player = self
        self.name = name
        self.sight = 10
        self.health = hp
        self.max_health = hp
        self.dead = False
        self.atk = 11

    def spawn(self):
        cx, cy = current_map.rooms[0].center()
        self.x = cx
        self.y = cy

    def move(self, dx, dy, speed=1):
        #move by the given amount
        if not current_map.tilemap[self.x + dx][self.y + dy].blocked \
                and not self.next_to_object(dx, dy) and not self.dead:
            self.x += dx+(speed-1)
            self.y += dy+(speed-1)

    def take_damage(self, amount):
        self.health -= amount
        msgbox.add_to_queue(("Your current health is: " + str(self.health) + "/" +
                             str(self.max_health), (255, 255, 255), None))
        if self.health <= 0:
            self.die()

    def die(self):
        global all_objects
        if self in all_objects:
            all_objects.remove(self)
        self.dead = True
        self.clear()

    def attack(self):
        neighboring_npcs = []
        global all_objects
        msgbox.add_to_queue(("You draw your blade...", (255, 255, 255), None))
        for obj in all_objects:
            if obj.x-1 <= self.x <= obj.x+1 and obj.y-1 <= self.y <= obj.y+1 and type(obj) is not type(self):
                if obj in neighboring_npcs:
                    pass
                else:
                    neighboring_npcs.append(obj)

        if neighboring_npcs:
            c2 = 0
            for npc in neighboring_npcs:
                msgbox.add_to_queue(("You attack the " + type(npc).__name__ + ".", (255, 255, 255), None))
                npc.take_damage(self.atk)
                if npc.dead:
                    c2 += 1
                    msgbox.add_to_queue(("The " + type(npc).__name__ + " is dead!", (255, 255, 255), None))
                c2 += 1
        else:
            msgbox.add_to_queue(("...and swing blindly in the dark.", (255, 255, 255), None))

    """
    def attack(self):
        neighboring_npcs = []
        global all_objects
        print("You begin to attack...")
        msgbox.draw_str(1,1, "You begin to attack...", fg=(255,255,255), bg=None)
        for obj in all_objects:
            if obj.x-1 <= self.x <= obj.x+1 and obj.y-1 <= self.y <= obj.y+1 and type(obj) is not type(self):
                if obj in neighboring_npcs:
                    print(f'not appending {type(obj).__name__} ({obj.x},{obj.y})')
                
                else:
                    neighboring_npcs.append(obj)
                    print(f'{type(obj).__name__} ({obj.x},{obj.y}) appended')
            #else:
                #

        if neighboring_npcs:
            print('You draw your blade...')
            self.msgbox.draw_str(1,2, "You draw your blade...", fg=(255,255,255), bg=None)
            line = 3
            for counter, npc in enumerate(neighboring_npcs):
                line += 1
                print('\t' + str(counter+1) + ': ' + type(npc).__name__ + ' - ' + str(npc.health) + '/' + str(npc.max_health))
                self.msgbox.draw_str(1,counter+3, f"\t{str(counter+1)}: {type(npc).__name__} - HP: {str(npc.health)}/{str(npc.max_health)}", fg=(255,255,255), bg=None)

            selected = 0
            self.msgbox.draw_str(1,line,"Choose a target to attack:")
            #selector = input("Choose a target to attack: ")
            s = tdl.event.key_wait()
            selector = s.key
            try:
                selected = int(selector)
                if selected-1 in range(0,len(neighboring_npcs)):
                    neighboring_npcs[selected-1].take_damage(self.atk)
                    self.msgbox.draw_str(1,line+1,f"You slash the {type(neighboring_npcs[selected-1]).__name__} with great force.")
            except:
                self.msgbox.draw_str(1,line+1,"You swing blindly in the dark.")
                    
            
            print('You attack the ' + type(neighboring_npcs[selected-1]).__name__)
        else:
            self.msgbox.draw_str(1,3, "...but nothing is near.", fg=(255,255,255), bg=None)
       """         
        

class NPC(GameObject):
    def __init__(self, health=10, attacks=False, atk=1):
        GameObject.__init__(self, '@', (255, 255, 0))
        self.sight = 10
        self.speed = 1
        self.health = health
        self.max_health = health
        self.dead = False
        self.attacks = attacks
        self.atk = atk

    def attack(self, target):
        if self.attacks:
            target.take_damage(self.atk)
            msgbox.add_to_queue(("The " + type(self).__name__ + " attacks!", (255, 255, 255), None))

    def take_damage(self, amount):
        self.health -= amount
        msgbox.add_to_queue(("The " + type(self).__name__ + "'s current health is: " +
                             str(self.health) + "/" + str(self.max_health), (255, 255, 255), None))
        if self.health <= 0:
            self.die()
            
    def die(self):
        global all_objects
        all_objects.remove(self)
        self.dead = True
        self.blocks = False
        if self.attacks:
            self.player.max_health += 10
            msgbox.add_to_queue(("The " + type(self).__name__ +
                                 " was slain. Your MaxHP goes up by 10!", (255, 255, 255), None))
        self.clear()

    def draw(self):
        #draw the character that represents this object at its position
        player_visible_tiles = tdl.map.quick_fov(self.player.x, self.player.y,
                                         self.current_map.is_visible_tile,
                                         fov='BASIC',
                                         radius=self.player.sight,
                                         lightWalls=False)
        if (self.x, self.y) in player_visible_tiles:
            self.con.draw_char(self.x, self.y, self.char, self.color)

    def move(self, dx, dy):
        #move by the given amount
        if not self.current_map.tilemap[self.x + (dx*self.speed)][self.y + (dy*self.speed)].blocked \
                and not self.next_to_object(dx, dy):
            self.x += dx*self.speed
            self.y += dy*self.speed

    def take_turn(self):
        if self.health > 0:
            randx = randint(-self.speed,self.speed)
            randy = randint(-self.speed,self.speed)
            if self.player.x-1 <= self.x <= self.player.x+1 and self.player.y-1 <= self.y <= self.player.y+1:
                self.attack(self.player)
            else:
                self.move(randx, randy)


class Monster(NPC):
    def __init__(self):
        NPC.__init__(self, 50, attacks=True, atk=10)
        GameObject.__init__(self, 'M', (0, 120, 120))
        self.sight = 16
        self.speed = 1
        self.dead = False

    def take_turn(self):
        if self.health > 0:
            randx = randint(-self.speed,self.speed)
            randy = randint(-self.speed,self.speed)
            if self.player_in_vision():
                if self.player.x-1 <= self.x <= self.player.x+1 and self.player.y-1 <= self.y <= self.player.y+1:
                    self.attack(self.player)
                else:
                    self.move_towards(self.player)
            else:
                self.move(randx, randy)

    def player_in_vision(self):
        visible_tiles = tdl.map.quick_fov(self.x, self.y,
                                         self.current_map.is_visible_tile,
                                         fov='BASIC',
                                         radius=self.sight,
                                         lightWalls=False)
        if (self.player.x, self.player.y) in visible_tiles:
            return True
        else:
            return False

    def move_towards(self, target):
            (dx, dy) = self.get_distance(target)
            self.move(dx*self.speed, dy*self.speed)


class HealthItem(GameObject):
    def __init__(self):
        GameObject.__init__(self, '+', (255, 0, 0))
        global all_objects
        all_objects.remove(self)
        self.dead = False

    def draw(self):
        player_visible_tiles = tdl.map.quick_fov(self.player.x, self.player.y,
                                         current_map.is_visible_tile,
                                         fov='BASIC',
                                         radius=self.player.sight,
                                         lightWalls=False)
        if (self.x, self.y) in player_visible_tiles:
            self.con.draw_char(self.x, self.y, self.char, self.color, (255,255,255))

    def take_turn(self):
        if self.player.x == self.x and self.player.y == self.y:
            if self.player.health == self.player.max_health:
                msgbox.add_to_queue(("You see a health item, but do not pick it up.", (255, 255, 255), None))
            else:
                self.player.health = self.player.max_health
                self.dead = True
                self.clear()
                msgbox.add_to_queue(("Your health has been fully restored!.", (255, 255, 255), None))


class PowerItem(GameObject):
    def __init__(self):
        GameObject.__init__(self, '*', (255, 255, 255), blocks=False)
        global all_objects
        all_objects.remove(self)
        self.dead = False

    def draw(self):
        player_visible_tiles = tdl.map.quick_fov(self.player.x, self.player.y,
                                         current_map.is_visible_tile,
                                         fov='BASIC',
                                         radius=self.player.sight,
                                         lightWalls=False)
        if (self.x, self.y) in player_visible_tiles:
            self.con.draw_char(self.x, self.y, self.char, self.color, (255, 0, 0))

    def take_turn(self):
        if self.player.x == self.x and self.player.y == self.y:
            self.player.atk += 1
            self.dead = True
            self.clear()
            msgbox.add_to_queue(("Your ATK has been improved!", (255, 255, 255), None))


class Portal(GameObject):
    def __init__(self):
        GameObject.__init__(self, 'O', (0, 64, 255), blocks=False)
        global all_objects
        all_objects.remove(self)

    def spawn(self):
        # set the current maximum coordinates to the player's position to start
        cxmax, cymax = current_map.rooms[0].center()

        #find the room most distant from the player's room whose center is still in bounds and not a wall tile
        for room in current_map.rooms:
            cx, cy = room.center()
            if (cx > cxmax or cy > cymax) and \
                    cx in range(2, current_map.width-1) and \
                    cy in range(2, current_map.height-1) and \
                    not current_map.tilemap[cx][cy].blocked:
                cxmax = cx
                cymax = cy

        #set the spawn point to the current maxmimum coordinates
        self.x = cxmax
        self.y = cymax
        print("Portal spawned at: " + str(self.x) + ", " + str(self.y))

    def debug_spawn(self):
        while True:
            self.x = randint(player.x-1, player.x+1)
            self.y = randint(player.y-1, player.y+1)
            if not current_map.tilemap[self.x][self.y].blocked:
                break

    def draw(self):
        player_visible_tiles = tdl.map.quick_fov(player.x, player.y,
                                         current_map.is_visible_tile,
                                         fov='BASIC',
                                         radius=player.sight,
                                         lightWalls=False)
        if (self.x, self.y) in player_visible_tiles:
            msgbox.add_to_queue(("The Portal is nearby!", (0, 64, 255), None))
            self.con.draw_char(self.x, self.y, self.char, self.color, None)

    def below_player(self):
        if self.x == player.x and self.y == player.y:
            return True
        return False
