# Simple pygame program

# Import and initialize the pygame library
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards

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

# Run until the user asks to quit
running = True
while running:


    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False



    # Fill the background with white
  
    screen.fill((0, 0, 0))

    sub_width = SCREEN_WIDTH-SCREEN_HEIGHT
    border_width = 5
    #grid_offset = 25
    grid_count = 8
    block_size = 73
    block_draw_size = block_size + 2

    offset = SCREEN_HEIGHT/2 - (grid_count*(block_size)/2)
                    
    for y in range(grid_count):
        for x in range(grid_count):
            
            pygame.draw.rect(
                screen,
                (222, 222, 222),
                (
                    sub_width + offset + (x * (block_size)), offset + (y * (block_size)),
                    block_draw_size, block_draw_size
                ),
                width=2
            )

    BSS = pygame.image.load("/home/dzarco@cpc.local/Downloads/Space Game/Blue Spaceship.png")
    width = BSS.get_rect().width
    height = BSS.get_rect().height
    BSS = pygame.transform.scale(BSS, (int(width)))

    screen.blit(BSS, (200,200))
    
  
 
    

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
    
    # Flip the display
    pygame.display.flip()

    clock.tick(60)

# Done! Time to quit.
pygame.quit()




























































































