# Imports

import pygame
import random
import os

# Set up game window
pygame.font.init() # Initialise fonts
WIDTH, HEIGHT= 750,750 # Choose window size
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Choose your caption")

# Load Assets
## Repeat as necessary
assets_dir = ''
asset_1 = pygame.image.load(
    os.path.join(assets_dir,img)
)

# Pick background image
BG = pygame.transform.scale(
   pygame.image.load(os.path.join(assets_dir, 'img')),
    (WIDTH, HEIGHT)
)

# Classes
## Mind your inheritance!

# Collision detectioni between two objects
def collision(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y) != None)

# Main loop
def main():
    # Set your variables
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("arial", 50)


    # Redraw window function
    def redraw_window():
        WIN.blit(BG, (0,0))
        ## Draw text
        lives_label = main_font.render(f"Lives: {lives} ", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level} ", 1, (255,255,255))
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        ## Draw player and enemies
        for enemy in enemies:
            enemy.draw(WIN)
        player.draw(WIN)
        if lost:
            lost_label = lost_font.render("You lost!!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 250))
            
    # While loop
    while run == True:
        # Tick the clock
        pygame.clock.tick()
        
        # Redraw the window
        redraw_window()

        # Test if game over
        if lost:
            lost_label = lost_font.render("You lost!!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 250))

        # Test enemies on field


        # Check for player input
        keys = pygame.keys.get_pressed()
        if keys[pygame.K_a]: # Left
            pass
        elif keys[pygame.K_d]: # Right
            pass
        elif keys[pygame.K_w]: # Up
            pass
        elif keys[pygame.K_s]: # Down
            pass
        elif keys[pygame.K_SPACE]: # Space
            pass

        # Execute actions

# Main menu
def main_menu():
    pass

main()
