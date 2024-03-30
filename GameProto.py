# Space Game

# Import and initialize the pygame library
import sysconfig
print(sysconfig.get_paths()["purelib"])
import pygame
import random

# Initialize Pygame Mixer
pygame.mixer.init()

# Load sound effects
death_sound = pygame.mixer.Sound("Sound Effects/psz_dead.mp3")
win_sound = pygame.mixer.Sound("Sound Effects/win_loud.mp3")
lose_sound = pygame.mixer.Sound("Sound Effects/gameover_loud.mp3")
damage_sound = pygame.mixer.Sound("Sound Effects/bomb.mp3")
attack_sound = pygame.mixer.Sound("Sound Effects/laser.mp3")


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    QUIT,
)

#Spaceships
pl_ship = pygame.image.load("Images/blueships1.png")
bswidth = pl_ship.get_rect().width
bsheight = pl_ship.get_rect().height
en_ship = pygame.image.load("Images/redfighter0005.png")
eswidth = en_ship.get_rect().width
esheight = en_ship.get_rect().height

#Motherships
pl_mothership = pygame.image.load("Images/WB_baseu3_d0.png")
bmwidth = pl_mothership.get_rect().width
bmheight = pl_mothership.get_rect().height
en_mothership = pygame.image.load("Images/tribase-u2-d0.png")
emwidth = en_mothership.get_rect().width
emheight = en_mothership.get_rect().height

targeting = False

# Base Class
class Unit:
    def __init__(self, pos, name, type=None):


        self.name = name
        self.position = pos  

        # Change stats depending on ship type. default to scout
        if(type=="Scout"):
            self.movement_range = 3
            self.attack_range = 2
            self.maxhealth = 100
            self.maxshields = 75
            self.attack = 50
            self.attacksleft = 1
        elif(type=="Mothership"):
            self.movement_range = 1
            self.attack_range = 3
            self.maxhealth = 500
            self.maxshields = 750
            self.attack = 100
            self.attacksleft = 1
        else:
            self.movement_range = 3
            self.attack_range = 2
            self.maxhealth = 100
            self.maxshields = 75
            self.attack = 100
            self.attacksleft = 1

        self.health = self.maxhealth
        self.shields = self.maxshields
        self.moves_left = self.movement_range


    def info(self):
        health_txt = "Health: " + str(self.health) + "/" + str(self.maxhealth)
        shields_txt = "Shields: " + str(self.shields) + "/" + str(self.maxshields)
        attack_txt = "Attack: " + str(self.attack)

        return [health_txt, shields_txt, attack_txt]

# Player Class
class Player(Unit):
    def __init__(self, pos, name, type=None):
        super().__init__(pos, name, type=type)
        if type == "Mothership":
            self.image = pl_mothership
        else:
            self.image = pl_ship
        self.team = "Player"

#Enemy Class
class Enemy(Unit):
    def __init__(self, pos, name, type=None):
        super().__init__(pos, name, type=type)
        if type == "Mothership":
            self.image = en_mothership
        else:
            self.image = en_ship
        self.team = "Enemy"

    # Movement control for enemies
    def make_move(self, entities, grid_count):
      valid_moves = [(x, y) for x in range(grid_count) for y in range(grid_count)]
      valid_moves = [move for move in valid_moves if all(thing.position != move for thing in entities)]

      if valid_moves:
          new_pos = random.choice(valid_moves)
          self.position = new_pos
      else:
          return None

# Function to check win condition 
def check_win_condition(entities):
    # Check if there are any enemies left
    enemies_remaining = any(entity for entity in entities if entity.team == "Enemy")
    if not enemies_remaining:
        win_sound.play()  # Play win sound
        print("YOU WON! All enemeies have been defeated! You have saved the galaxy!")


# Function to check lose condition
def check_lose_condition(entities):
    # Check if there are any player ships left
    player_ships_remaining = any(entity for entity in entities if entity.team == "Player" and entity.health > 0)
    if not player_ships_remaining:
        lose_sound.play()  # Play lose sound
        print("YOU LOST! All your ships have been destroyed! The galaxy is doomed! GAME OVER!")

# Maybe add a map class
class Map:
    def __init__(self):
        pass

def draw(self, screen, sub_width, offset):
    for entity in entities:
        currPos = entity.position
        screen.blit(self.image, (sub_width + currPos[0]*block_size + offset, currPos[1]*block_size + offset))

# dist between two map points
def calcDist(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

# show valid ship movement and attacking locations
nabes = [(0,1),(1,0),(0,-1),(-1,0)]

def shipSelection(currShip):
    pos = currShip.position
    move_highlight.clear()
    move_highlight.append(pos)
    attack_highlight.clear()
    search=[(pos, current_ship.moves_left)]
    search2=[]
    done=set()
    if currShip.team == "Player":
        targeting = True
    while search:
        currPos, moves = search.pop(0)
        if(currPos in done):
            continue
        if(moves <= 0):
            search2.append([currPos,current_ship.attack_range])
            continue
        done.add(currPos)
        for nabe in nabes:
            xx,yy = (currPos[0]+nabe[0],currPos[1]+nabe[1])
            if(xx>=0 and yy>=0 and xx < grid_count and yy < grid_count and (xx,yy) not in done):
                if(all(thing.position!=(xx,yy) for thing in entities)):
                    move_highlight.append((xx,yy))
                    search.append(((xx,yy),moves-1))

    while search2:
        currPos, atk = search2.pop(0)
        if(currPos in done or atk <= 0):
            continue
        done.add(currPos)
        for nabe in nabes:
            xx,yy = (currPos[0]+nabe[0],currPos[1]+nabe[1])
            if(xx>=0 and yy>=0 and xx < grid_count and yy < grid_count and (xx,yy) not in done):
                attack_highlight.append((xx,yy))
                search2.append(((xx,yy),atk-1))
                
                
def attack(ship, unit):
    atk = ship.attack
    attack_sound.play()  # Play attack sound for every attack
    if unit.shields < atk and unit.health > 0:
        damage_sound.play()  # Play taking damage sound if the unit survives
    if unit.shields < atk:
        bonus_atk = atk - unit.shields
        unit.shields = 0 
        unit.health -= bonus_atk
    else:
        unit.shields -= atk
    if unit.health < 0:
        unit.health = 0
        death_sound.play()  # Play death sound
   


### GAME INITIALIZATION ###
pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
# Set up the drawing window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

entities=[]
entities.append(Player((5,3), "Player Ship 1"))    
entities.append(Player((2,6), "Player Ship 2"))
# Enemy's
entities.append(Enemy((2,3), "Enemy Ship 1"))    
entities.append(Enemy((4,2), "Enemy Ship 2"))

entities.append(Player((5, 7), "Blue Mothership", type="Mothership"))
entities.append(Enemy((2, 0), "Red Mothership", type="Mothership"))

move_highlight=[]
attack_highlight=[]
selection_highlight=[]
selection=None
previous=None
current_ship = None
tagged_ship = None
info = None
disp_info = []
current_player = "Player1"

sub_width = SCREEN_WIDTH-SCREEN_HEIGHT
border_width = 5
grid_count = 8
block_size = 75
offset = SCREEN_HEIGHT/2 - (grid_count*(block_size)/2)

running = True

def enemy_move_and_attack(entities, grid_count):
    for entity in entities:
        if entity.team == "Enemy":
            entity.make_move(entities, grid_count)
            for target in entities:
                if target.team == "Player" and target.health > 0 and entity.health > 0 and calcDist(entity.position, target.position) <= entity.attack_range:
                    print(f"{entity.name} attacks {target.name}!")
                    attack(entity, target)
                    if target.health <= 0:
                        print(f"{target.name} has been destroyed!")
                    

while running:
    
    mousex, mousey = pygame.mouse.get_pos()
    mousexx = round((mousex - sub_width - offset - block_size/2)/block_size)
    mouseyy = round((mousey - offset - block_size/2)/block_size)

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_RETURN:
                enemy_move_and_attack(entities, grid_count)
                check_win_condition(entities)  # checking win condition after enemy action
                check_lose_condition(entities)  # checking lose condition after enemy action
                # Restting move count for players ships
                for entity in entities:
                    if entity.team == "Player":
                        entity.moves_left = entity.movement_range
                        check_win_condition(entities)  # checking win condition after player has reset
                        check_lose_condition(entities)  # checking lose condition after player has reset
                print("Your turn to move!")
                for entity in entities:
                    entity.attacksleft = 1

        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if mousexx >= 0 and mouseyy >= 0 and mousexx < grid_count and mouseyy < grid_count:
                    previous = current_ship
                    selection = (mousexx, mouseyy)
                    print(selection)

                    for entity in entities:
                        if entity.position == selection:
                            new_selection = True
                            current_ship = entity
                            info = entity.info()
                            break
                    if previous != None and current_ship.team != None:
                        if previous.team == "Player" and current_ship.team == "Enemy":
                            if previous.attacksleft > 0:
                                attack(previous, current_ship)
                                previous.attacksleft -= 1
                    if new_selection:
                        shipSelection(current_ship)
                        if selection in move_highlight and current_ship.team == "Player":
                            dist = calcDist(selection, current_ship.position)
                            current_ship.moves_left -= dist
                            current_ship.position = selection
                            shipSelection(current_ship)
                            check_win_condition(entities)  # checking win condition after player action
                            check_lose_condition(entities) # checking lose condition after player action
                # The end turn button have been pressed
                elif end_turn_button_rect.collidepoint(mousex, mousey):
                    enemy_move_and_attack(entities, grid_count)
                    check_win_condition(entities)  # Checking win condition after enemy action
                    check_lose_condition(entities)  # Checking lose condition after enemy action
                    print("Enemy's turn!")
                    for entity in entities:
                        if entity.team == "Player":
                            entity.moves_left = entity.movement_range
                    print("Your turn to move!")

    screen.fill((0, 0, 0))

    # Draw menu borders
    pygame.draw.rect(screen, (100, 100, 255), (0, 0, sub_width, SCREEN_HEIGHT), width=border_width)
    pygame.draw.rect(screen, (100, 100, 255), (sub_width, 0, SCREEN_HEIGHT, SCREEN_HEIGHT), width=border_width)

    end_turn_button_rect = pygame.Rect(20, SCREEN_HEIGHT - 50, 100, 30)

    # Draw End button 
    pygame.draw.rect(screen, (50, 50, 50), end_turn_button_rect)
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    end_turn_text = pygame.font.Font.render(font, "End Turn", True, (255, 255, 255))
    screen.blit(end_turn_text, (end_turn_button_rect.x + 10, end_turn_button_rect.y + 5))

    offset = SCREEN_HEIGHT/2 - (grid_count*(block_size)/2)

    #UI Text
    font = pygame.font.Font(pygame.font.get_default_font(), 24)
    if current_ship is not None:
        name = pygame.font.Font.render(font, current_ship.name, True, (255, 255, 255))
        display_image = pygame.transform.scale(current_ship.image, (200, 200))
        if disp_info != []:
            disp_info = []
        for stat in info:
            disp_info.append(pygame.font.Font.render(font, stat, True, (255, 255, 255)))

        screen.blit(name, (20, 20))
        screen.blit(display_image, (55, 50))
        txtpos = 0
        i = 0
        for stat in disp_info:
            txtpos += 50
            screen.blit(disp_info[i], (20, (sub_width + txtpos)))
            i += 1
        # if current_ship.team == Enemy and current_ship.position in any(entity.attack_ for entity in entities if entity.team == "Enemy")

    # Draw Grid
    for y in range(grid_count):
        for x in range(grid_count):
            grid_color = (222, 222, 222)
            pygame.draw.rect(
                screen,
                grid_color,
                (
                    sub_width + offset + (x * (block_size)), offset + (y * (block_size)),
                    block_size, block_size
                ),
                width=2
            )

    # highlight movement squares
    for x, y in move_highlight:
        grid_color = (100, 100, 255, 100)
        pygame.draw.rect(
            screen,
            grid_color,
            (
                sub_width + offset + (x * (block_size)), offset + (y * (block_size)),
                block_size, block_size
            ),
            width=2
        )

    # highlight attack squares
    for x, y in attack_highlight:
        grid_color = (255, 100, 100, 100)
        pygame.draw.rect(
            screen,
            grid_color,
            (
                sub_width + offset + (x * (block_size)), offset + (y * (block_size)),
                block_size, block_size
            ),
            width=2
        )

    #selection highlight
    for x, y in selection_highlight:
        grid_color = (255, 255, 100, 100)
        pygame.draw.rect(
            screen,
            grid_color,
            (
                sub_width + offset + (x * (block_size)), offset + (y * (block_size)),
                block_size, block_size
            ),
            width=2
        )


    # show mouse-selected grid square
    mousex, mousey = pygame.mouse.get_pos()
    mousexx = (mousex - sub_width - offset - block_size/2)/block_size
    mouseyy = (mousey - offset - block_size/2)/block_size
    if mousexx > -0.5 and mouseyy > -0.5 and mousexx < grid_count - 0.5 and mouseyy < grid_count - 0.5:
        pygame.draw.rect(
            screen,
            (200, 200, 0),
            (
                round(mousexx) * block_size + (sub_width + offset), 
                round(mouseyy) * block_size + offset,
                block_size, block_size
            ),
            width=5
        )

    ### Map Entities ###
    for entity in entities:
        if entity.health > 0:
          currPos = entity.position
          image = pygame.transform.scale(entity.image, (block_size, block_size))
          screen.blit(image, 
            (sub_width + currPos[0] * block_size + offset, 
            currPos[1] * block_size + offset)
        )


    # Flip the display
    pygame.display.flip()

    clock.tick(60)

# Done! Time to quit.
pygame.quit()
