# Simple pygame program

# Import and initialize the pygame library
import sysconfig
import pygame
import random  # Add this for random enemy movement

print(sysconfig.get_paths()["purelib"])

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards

pl_ship = pygame.image.load("untitledspacegame-enemy-moving/Images/BlueSpaceship.png")
en_ship = pygame.image.load("untitledspacegame-enemy-moving/Images/RedSpaceship.png")



class Unit:
    def __init__(self, pos, name, type=None):
        self.name = name
        self.position = pos
        self.image = pl_ship if type == "Player" else en_ship
        self.team = type
        self.movement_range = 3
        self.attack_range = 2
        self.health = 100
        self.maxhealth = 100
        self.shields = 75
        self.maxshields = 75
        self.attack = 10

    def info(self):
        health_txt = "Health: " + str(self.health) + "/" + str(self.maxhealth)
        shields_txt = "Shields: " + str(self.shields) + "/" + str(self.maxshields)
        attack_txt = "Attack: " + str(self.attack)
        return [health_txt, shields_txt, attack_txt]

class Enemy(Unit):
    # Inherits from Unit, no changes needed here as we've combined Unit and Enemy functionality

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
pygame.font.init()  # This line initializes the font module.
clock = pygame.time.Clock()
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define font
font_size = 24
font = pygame.font.SysFont(None, font_size)  # Now 'font' is defined and can be used


# Initialize your player and enemy units here
entities = [
    Unit((4, 7), "Player Ship 1", "Player"),
    Unit((2, 6), "Player Ship 2", "Player"),
    Unit((2, 3), "Enemy Ship 1", "Enemy"),
    Unit((4, 2), "Enemy Ship 2", "Enemy")
]

move_highlight = []
attack_highlight = []
selection = None
current_ship = None
info = None
disp_info = []

sub_width = SCREEN_WIDTH - SCREEN_HEIGHT
border_width = 5
grid_count = 8
block_size = 73
offset = SCREEN_HEIGHT / 2 - (grid_count * block_size / 2)
nabes = [(0, 1), (1, 0), (0, -1), (-1, 0)]

player_turn = True  # Added to control turn sequence

# Here we add the enemy_move and enemy_attack functions
def enemy_move(entity, entities, grid_count):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dx, dy = random.choice(directions)
    new_position = (entity.position[0] + dx, entity.position[1] + dy)
    if 0 <= new_position[0] < grid_count and 0 <= new_position[1] < grid_count and not any(e.position == new_position for e in entities):
        entity.position = new_position

def enemy_attack(entity, entities):
    for target in entities:
        if target.team == "Player" and max(abs(entity.position[0] - target.position[0]), abs(entity.position[1] - target.position[1])) <= entity.attack_range:
            print(f"{entity.name} attacks {target.name}!")
            target.health -= entity.attack
            break  # Each enemy attacks once per turn

# Game loop starts here
running = True
while running:
    mousex, mousey = pygame.mouse.get_pos()
    mousexx = round((mousex - sub_width - offset - block_size / 2) / block_size)
    mouseyy = round((mousey - offset - block_size / 2) / block_size)

    # Event handling
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            # Ensure actions are processed only during the player's turn
            if player_turn:
                if(mousexx>=0 and mouseyy>=0 and mousexx < grid_count and mouseyy < grid_count):
                    selection = (mousexx, mouseyy)
                    new_selection = False
                    for entity in entities:
                        if entity.position == selection:
                            new_selection = True
                            current_ship = entity
                            info = entity.info()
                            break
                    if new_selection:
                        move_highlight.clear()
                        attack_highlight.clear()
                        # Logic for highlighting move and attack options would go here
                    else:
                        # Logic for moving the selected ship to a new location
                        if selection in move_highlight and current_ship.team == "Player":
                            current_ship.position = selection
                player_turn = False  # End the player's turn after they take an action

    # AI Turn logic
    if not player_turn:
        for entity in entities:
            if entity.team == "Enemy":
                enemy_move(entity, entities, grid_count)
                enemy_attack(entity, entities)
        player_turn = True  # Hand turn back to player after all enemies have acted

    # Clear the screen
    screen.fill((0, 0, 0))

        # Drawing and Rendering:

    # Clear the screen to black
    screen.fill((0, 0, 0))

    # Draw menu and grid borders
    pygame.draw.rect(screen, (100, 100, 255), (0, 0, sub_width, SCREEN_HEIGHT), border_width)
    pygame.draw.rect(screen, (100, 100, 255), (sub_width, 0, SCREEN_HEIGHT, SCREEN_HEIGHT), border_width)

    # Draw the grid
    for y in range(grid_count):
        for x in range(grid_count):
            pygame.draw.rect(
                screen,
                (222, 222, 222),
                (sub_width + offset + x * block_size, offset + y * block_size, block_size, block_size),
                width=2
            )

    # Draw move and attack highlights
    for x, y in move_highlight:
        pygame.draw.rect(
            screen,
            (100, 100, 255),
            (sub_width + offset + x * block_size, offset + y * block_size, block_size, block_size),
            width=3
        )
    for x, y in attack_highlight:
        pygame.draw.rect(
            screen,
            (255, 100, 100),
            (sub_width + offset + x * block_size, offset + y * block_size, block_size, block_size),
            width=3
        )

    # Draw entities (ships)
    for entity in entities:
        image = pygame.transform.scale(entity.image, (block_size, block_size))
        screen.blit(
            image,
            (sub_width + entity.position[0] * block_size + offset,
             entity.position[1] * block_size + offset)
        )

    # UI Text for the current ship
    if current_ship:
        ship_info = current_ship.info()
        ship_name = font.render(current_ship.name, True, (255, 255, 255))  # Uses the 'font' object to render text
        screen.blit(ship_name, (20, 20))
        for i, info_text in enumerate(ship_info):
            info_surf = font.render(info_text, True, (255, 255, 255))  # Fixed: 'font.render' instead of just 'render'
            screen.blit(info_surf, (20, 50 + i * 30))

    # Update the display and tick the clock
    pygame.display.flip()
    clock.tick(60)

# Cleanup and exit
pygame.quit()
