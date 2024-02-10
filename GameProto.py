# Simple pygame program

# Import and initialize the pygame library
import sysconfig
print(sysconfig.get_paths()["purelib"])
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
font = pygame.font.Font(pygame.font.get_default_font(), 24)

class Unit:
    def __init__(self, pos, type=None):
        self.position = pos
        
class Ship:
    def __init__(self, 
                pos,
                name,
                health, 
                max_health,
                shields,
                max_shields,
                attack,
                type=None):
        self.position = pos
        self.name = name
        self.health = health
        self.max_health = max_health
        self.shields = shields
        self.max_shields = max_shields
        self.attack = attack
    
        def info(self):
            ship_txt = "Current Ship: " + self.name
            health_txt = "Health: " + str(self.health) + "/" + str(self.max_health)
            shields_txt = "Shields: " + str(self.shields) + "/" + str(self.max_shields)
            attack_txt = "Attack: " + str(self.attack)
            
            return [ship_txt, health_txt, shields_txt, attack_txt]



class Map:
    def __init__(self):
        pass


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    QUIT,
)

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
# Set up the drawing window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


ship = Ship((2,6),"Ship 1", 50, 100, 75, 75, 20)
ship = Ship((4,2),"Ship 1", 50, 100, 75, 75, 20)
entities=[]
entities.append(ship)    
entities.append(ship)

highlight=[]
selection=None

sub_width = SCREEN_WIDTH-SCREEN_HEIGHT
border_width = 5
#grid_offset = 25
grid_count = 8
block_size = 73
block_draw_size = block_size + 2
selected = False


offset = SCREEN_HEIGHT/2 - (grid_count*(block_size)/2)

nabes = [(0,1),(1,0),(0,-1),(-1,0)]
# Run until the user asks to quit
running = True
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
        if event.type == pygame.QUIT:
            running = Facurrent_ship = "Current Ship"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(pygame.mouse.get_pressed()[0]):
                if(mousexx>=0 and mouseyy>=0 and mousexx < grid_count and mouseyy < grid_count):
                    previous = selection
                    selection = (mousexx,mouseyy)
                    if(any([selection==x.position for x in entities])):
                        selected == True
                        info = x.info()
                        highlight.clear()
                        highlight.append(selection)
                        for nabe in nabes:
                            xx,yy = (selection[0]+nabe[0],selection[1]+nabe[1])
                            if(xx>=0 and yy>=0 and xx < grid_count and yy < grid_count):
                                highlight.append((xx,yy))





    # Fill the background with white
    screen.fill((0, 0, 0))



    sub_width = SCREEN_WIDTH-SCREEN_HEIGHT
    border_width = 5
    #grid_offset = 25
    grid_count = 8
    block_size = 73
    block_draw_size = block_size + 2

    offset = SCREEN_HEIGHT/2 - (grid_count*(block_size)/2)

    # Draw menu borders
    pygame.draw.rect(screen, (100, 100, 255), (0, 0, sub_width, SCREEN_HEIGHT), width=border_width)
    pygame.draw.rect(screen, (100, 100, 255), (sub_width, 0, SCREEN_HEIGHT, SCREEN_HEIGHT), width=border_width)

  



    if selected == True:
        i = 0
        for stat in info:
            display = pygame.font.Font.render(font, stat, True, (255, 255, 255))
            if i == 0:
                screen.blit(display, (20, 20)) 
            else:
                screen.blit(display, (20, sub_width + i))
                i += 50  


    for y in range(grid_count):
        for x in range(grid_count):
            grid_color = (222, 222, 222)

            pygame.draw.rect(
                screen,
                grid_color,
                (
                    sub_width + offset + (x * (block_size)), offset + (y * (block_size)),
                    block_draw_size, block_draw_size
                ),
                width=2
            )

    for x,y in highlight:
        grid_color = (100, 100, 255, 100)
        pygame.draw.rect(
            screen,
            grid_color,
            (
                sub_width + offset + (x * (block_size)), offset + (y * (block_size)),
                block_draw_size, block_draw_size
            ),
            width=2
        )

    #Map Entities
    for entity in entities:
        currPos = entity.position
        pygame.draw.circle(screen, (100,100,255), 
            (sub_width + currPos[0]*block_size + offset + block_size/2, currPos[1]*block_size + offset + block_size/2),
            block_size*0.35)

    mousexx = round((mousex - sub_width - offset - block_size/2)/block_size)
    mouseyy = round((mousey - offset - block_size/2)/block_size)

    # Draw menu borders
    pygame.draw.line(screen, (100, 100, 255), (0, (sub_width * (4/5))), (sub_width, (sub_width * (4/5))), width=border_width)
    pygame.draw.rect(screen, (100, 100, 255), (0, 0, sub_width, SCREEN_HEIGHT), width=border_width)
    pygame.draw.rect(screen, (100, 100, 255), (sub_width, 0, SCREEN_HEIGHT, SCREEN_HEIGHT), width=border_width)


    mousex, mousey = pygame.mouse.get_pos()
    mousexx = (mousex - sub_width - offset - block_size/2)/block_size
    mouseyy = (mousey - offset - block_size/2)/block_size
    if(mousexx > -0.5 and mouseyy > -0.5 and mousexx < grid_count-0.5 and mouseyy < grid_count-0.5):
        pygame.draw.rect(
                screen,
                (200, 200, 0),
                (
                    round(mousexx)*block_size + (sub_width + offset), 
                    round(mouseyy)*block_size + offset,
                    block_draw_size, block_draw_size
                ),
                width=0
            )

    # Flip the display

    pygame.display.flip()

    clock.tick(60)
# Done! Time to quit.
pygame.quit()


