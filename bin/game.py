import tdl #fuck you pycharm this is an absolutely neccesary import
import random
from gameobject import *
from gamemap import *
import messagebox

steps = 0

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 75
CON_WIDTH = (SCREEN_WIDTH*4)//5
CON_HEIGHT = (SCREEN_HEIGHT*4)//5
HUD_WIDTH = SCREEN_WIDTH//5
HUD_HEIGHT = (SCREEN_HEIGHT*4)//5
MSG_WIDTH = SCREEN_WIDTH
MSG_HEIGHT = SCREEN_WIDTH//5
playerx = SCREEN_WIDTH//2
playery = SCREEN_HEIGHT//2

root = None
con = None
hud = None
msgbox = None
player = None

#===============================================================================


def draw_end_screen(message):
    hud.draw_rect(0, 0, None, None, None, fg=(0, 0, 0), bg=(0, 0, 0))
    msgbox.console.draw_rect(0, 0, None, None, None, fg=(0, 0, 0), bg=(0, 0, 0))
    con.draw_rect(0, 0, None, None, None, fg=(0, 0, 0), bg=(0, 0, 0))
    con.draw_frame((SCREEN_WIDTH//2)-(len(message)//2)-2, (SCREEN_HEIGHT//2)-2, len(message)+4, 5, None,
                   fg=(255, 255, 255), bg=(255, 255, 255))
    con.draw_str((SCREEN_WIDTH//2)-(len(message)//2), SCREEN_HEIGHT//2, message, fg=(255, 255, 255), bg=(0, 0, 0))


def draw_hud(objects):
    global steps, player
    hud.draw_rect(0, 0, None, None, None, fg=(255, 255, 255), bg=(64, 64, 64))
    hud.draw_str(1, 1, player.name, fg=(255, 0, 255), bg=None)
    hud.draw_str(1, 2, "Position: (" + str(player.x) + "," + str(player.y) + ")", fg=(255, 255, 255), bg=None)
    hud.draw_str(1, 3, "Steps: " + str(steps), fg=(255, 255, 255), bg=None)
    hud.draw_str(1, 4, "HP: " + str(player.health) + "/" + str(player.max_health), fg=(255, 255, 255), bg=None)
    hud.draw_str(1, 5, "ATK: " + str(player.atk), bg=None)

    for counter, obj in enumerate(objects):
        if type(obj) is Monster:
            type_of_obj = 'MON'
            color = (0, 128, 128)
        else:
            type_of_obj = 'NPC'
            color = (255, 255, 0)
        hud.draw_str(1, 4*(counter+2)-1, '#' + str(counter+1) + ': ', fg=(255, 255, 255), bg=None)
        hud.draw_str(5, 4*(counter+2)-1,  type_of_obj, fg=color, bg=None)
        hud.draw_str(1, 4*(counter+2),  "HP: " + str(obj.health), fg=(255, 255, 255), bg=None)
        #hud.draw_str(1,6*(counter+2)-1, "Position: (" + str(obj.x) + "," + str(obj.y) + ")", fg=(255,255,255), bg=None)


def clear_hud():
    for i in range(1, hud.height):
        hud.draw_str(1, i, " "*19, fg=(255, 255, 255), bg=None)

#===============================================================================


def create_objects():
    objects = []
    size = random.randint(4, 10)
    for i in range(1, size):
        chance = random.randint(1, 100)
        if chance <= 40:
            objects.append(Monster())
        else:
            objects.append(NPC())
    return objects


def create_items():
    items = []
    size = random.randint(5, 20)
    for i in range(1, size):
        chance = random.randint(1, 100)
        if chance <= 25:
            items.append(PowerItem())
        else:
            items.append(HealthItem())
    return items


#===============================================================================


def handle_keys():
    global player, con, steps
    user_input = tdl.event.key_wait()
    msgbox.clear_message()

    #movement keys
    if (user_input.key == 'UP' or user_input.key == 'KP8')and player.y >= 1:
        player.move(0, -1)
        steps += 1

    elif (user_input.key == 'DOWN' or user_input.key == 'KP2')and player.y < CON_HEIGHT-1:
        player.move(0, 1)
        steps += 1

    elif (user_input.key == 'LEFT' or user_input.key == 'KP4') and player.x >= 1:
        player.move(-1, 0)
        steps += 1

    elif (user_input.key == 'RIGHT' or user_input.key == 'KP6') and player.x < CON_WIDTH-1:
        player.move(1, 0)
        steps += 1

    elif user_input.key == 'KP7' and (player.x >= 1 and player.y >= 1): #northwest
        player.move(-1, -1)
        steps += 1

    elif user_input.key == 'KP9' and (player.x < CON_WIDTH-1 and player.y >= 1): #northeast
        player.move(1, -1)
        steps += 1
    
    elif user_input.key == 'KP1' and (player.x >= 1 and player.y < CON_HEIGHT-1): #southwest
        player.move(-1, 1)
        steps += 1

    elif user_input.key == 'KP3' and (player.x < CON_WIDTH-1 and player.y < CON_HEIGHT-1): #southeast
        player.move(1, 1)
        steps += 1
    
    elif user_input.key == 'KP0' and (1 < player.x < CON_WIDTH-1 and 1 < player.y < CON_HEIGHT-1): #wait
        player.attack()
        steps += 1

    elif user_input.key == 'KPDEC':
        msgbox.add_to_queue(("PLAYER STATUS:", (255, 255, 255), None))
        msgbox.add_to_queue(("    Health: " + str(player.health) + "/" + "str(player.max_health)", (255, 255, 255), None))
        msgbox.add_to_queue(("    Attack: " + str(player.atk), (255, 255, 255), None))

    elif user_input.key == 'F4' and user_input.alt:
        return True       
    
    else:
        msgbox.add_to_queue(("WARNING: The command was not recognized.", (255, 255, 0), None))
        print("command not recognized")
        steps += 1

#================================================================================


def run_game():
    global player, playerx, playery, root, con, hud, msgbox

    maps = []
    for i in range(1, 6):
        maps.append(GameMap(CON_WIDTH, CON_HEIGHT, palettes['grey'], con))

    gameobject.initialize_for_all(con, msgbox) 
    player = Player('Player')
    portal = Portal()
    gameobject.set_player(player)

    game_close = False    

    #runtime loop
    while not tdl.event.is_window_closed():

        for map_id, m in enumerate(maps):
               
            gameobject.set_map(m)
            #print(id(m))
            #print(id(gameobject.current_map))
            if map_id > 0:
                msgbox.add_to_queue(("You advance to the next level...", (255, 255, 255), None))
            else:
                msgbox.add_to_queue(("CONTROLS:", (255, 255, 255), None))
                msgbox.add_to_queue(("*Arrow keys OR Numpad 1-9: Move", (255, 255, 255), None))
                msgbox.add_to_queue(("*Numpad 0: ............... Attack", (255, 255, 255), None))
                msgbox.add_to_queue(("*Numpad Dot (.): ......... Show stats", (255, 255, 255), None))
                msgbox.add_to_queue((" ", (255, 255, 255), None))
                msgbox.add_to_queue(("HOW TO PLAY:",(255, 255, 255), None))
                msgbox.add_to_queue(("Find the portal to get to the next level.", (255, 255, 255), None))
                msgbox.add_to_queue((" ", (255, 255, 255), None))
                msgbox.add_to_queue(("Thank you for playing!", (255, 255, 255), None))
                msgbox.add_to_queue((" ", (255, 255, 255), None))
                                    
            player.spawn()
            portal.spawn()
                            
            objects = create_objects()
            items = create_items()

            for obj in objects:
                obj.spawn()
            for item in items:
                item.spawn()

            while not portal.below_player():
                m.clear()
                objects = [obj for obj in objects if not obj.dead]
                items = [item for item in items if not item.dead]
                
                for obj in objects:
                    obj.clear()
                    obj.take_turn()
                    obj.draw()
                for item in items:
                    item.clear()
                    item.take_turn()
                    item.draw()

                clear_hud()
                draw_hud(objects)
                msgbox.draw_msgbox()
                msgbox.print_queue()

                player.draw()
                portal.draw()
                
                m.draw(player)

                if game_close:
                    clear_hud()
                    for obj in objects:
                        obj.clear()
                    for item in items:
                        item.clear()
                    player.clear()
                    portal.clear()
                    msgbox.clear_message()
                    draw_end_screen("You may now close the console.")

                if player.dead:
                    clear_hud()
                    for obj in objects:
                        obj.clear()
                    for item in items:
                        item.clear()
                    player.clear()
                    portal.clear()
                    msgbox.clear_message()
                    draw_end_screen("You have died.")

                root.blit(con, 0, 0, CON_WIDTH, CON_HEIGHT, 0, 0) #first 4/5ths
                root.blit(hud, CON_WIDTH, 0, HUD_WIDTH, HUD_HEIGHT, 0, 0) #last 5th
                root.blit(msgbox.console, 0, CON_HEIGHT, MSG_WIDTH, MSG_HEIGHT, 0, 0)

                tdl.flush()

                player.clear()
                portal.clear()
                    
                if game_close or player.dead:
                    return
                game_close = handle_keys()
                
            #end while
        #end for

        clear_hud()
        msgbox.clear_message()
        player.clear()
        draw_end_screen("You won! Congrats!")
        root.blit(con, 0, 0, CON_WIDTH, CON_HEIGHT, 0, 0) #first 4/5ths
        root.blit(hud, CON_WIDTH, 0, HUD_WIDTH, HUD_HEIGHT, 0, 0) #last 5th
        root.blit(msgbox.console, 0, CON_HEIGHT, MSG_WIDTH, MSG_HEIGHT, 0, 0)
        tdl.flush()
        return
            #print(steps)
         #print(str(player.x) + ', ' + str(player.y))
         #print('ID of subcon: ' + str(id(con)))


#================================================================================
#MAIN FUNCTION
#================================================================================

def main():
    global SCREEN_HEIGHT, SCREEN_WIDTH, root, con, hud, msgbox

    tdl.set_font('terminal8x8_gs_tc.png', greyscale=True, altLayout=True)
    tdl.event.set_key_repeat(delay=1000, interval=1000)
    root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Very Small Roguelike", fullscreen=False)
    con = tdl.Console(CON_WIDTH, CON_HEIGHT)
    hud = tdl.Console(HUD_WIDTH, HUD_HEIGHT)
    msgbox = messagebox.MessageBox(tdl.Console(MSG_WIDTH, MSG_HEIGHT))
    run_game()

if __name__ == '__main__':
    print("You should be running this via loader.bat(Windows) or loader.sh(Mac/Linux).")
    print("However, if you're sure everything is installed, you can run it from here.")
    while True:
        okay = input("Do you wish to continue? (y/n): ")
        if okay == 'y' or okay == 'Y':
            print('\n\n\n')
            main()
            break
        elif okay == 'n' or okay == 'N':
            print('Goodbye!')
            break
        else:
            print('Invalid input.')
