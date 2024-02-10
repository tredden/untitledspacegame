# Simple pygame program

# Import and initialize the pygame library
import sysconfig
print(sysconfig.get_paths()["purelib"])
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
class Unit:
    def __init__(self, pos, type=None):
        self.position = pos

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
    QUIT,
)

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
# Set up the drawing window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

entities=[]
entities.append(Unit((4,7)))    
entities.append(Unit((2,6)))

highlight=[]
selection=None

sub_width = SCREEN_WIDTH-SCREEN_HEIGHT
border_width = 5
#grid_offset = 25
grid_count = 8
block_size = 73
block_draw_size = block_size + 2

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
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(pygame.mouse.get_pressed()[0]):
                if(mousexx>=0 and mouseyy>=0 and mousexx < grid_count and mouseyy < grid_count):
                    previous = selection
                    selection = (mousexx,mouseyy)
                    print(selection)
                    if(any([selection==x.position for x in entities])):
                        highlight.clear()
                        highlight.append(selection)
                        for nabe in nabes:
                            xx,yy = (selection[0]+nabe[0],selection[1]+nabe[1])
                            if(xx>=0 and yy>=0 and xx < grid_count and yy < grid_count):
                                highlight.append((xx,yy))


    current_ship = "Current Ship"

    health = 100
    max_health = 100
    shields = 75
    max_shields = 75
    attack = 10

    # Fill the background with white

    current_ship = "Current Ship"

    health = 100
    max_health = 100
    shields = 75
    max_shields = 75
    attack = 10

    health_txt = "Health: " + str(health) + "/" + str(max_health)
    shields_txt = "Shields: " + str(shields) + "/" + str(max_shields)
    attack_txt = "Attack: " + str(attack)


    screen.fill((0, 0, 0))

    sub_width = SCREEN_WIDTH-SCREEN_HEIGHT
    border_width = 5
    #grid_offset = 25
    grid_count = 8
    block_size = 73
    block_draw_size = block_size + 2

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

    #UI Text
    font = pygame.font.Font(pygame.font.get_default_font(), 24)
    ship_display = pygame.font.Font.render(font, current_ship, True, (255, 255, 255))
    health_display =  pygame.font.Font.render(font, health_txt , True, (255, 255, 255))
    shields_display =  pygame.font.Font.render(font, shields_txt, True, (255, 255, 255))
    attack_display =  pygame.font.Font.render(font, attack_txt, True, (255, 255, 255))

    screen.blit(ship_display, (20, 20))
    screen.blit(health_display, (20, (sub_width + 50)))
    screen.blit(shields_display, (20, (sub_width + 100)))
    screen.blit(attack_display, (20, (sub_width + 150)))   

    for y in range(grid_count):
        for x in range(grid_count):
            grid_color = (222, 222, 222)

            pygame.draw.rect(
                screen,
                (222, 222, 222),
                (
                    sub_width + offset + (x * (block_size)), offset + (y * (block_size)),
                    block_draw_size, block_draw_size
                ),
                width=2
            )

   
    
  
 
    

    # Draw menu borders
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
    BSS = pygame.image.load("./Images/Blue Spaceship.png")
    width = BSS.get_rect().width
    height = BSS.get_rect().height
    BSS = pygame.transform.scale(BSS, (block_size,block_size))

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

    for entity in entities:    
        currPos = entity.position
        screen.blit( BSS, 
            (sub_width + currPos[0]*block_size + offset, 
            currPos[1]*block_size + offset)
        )
    
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














