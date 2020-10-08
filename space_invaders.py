# This is the main.py script

import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
RED_SPACE_SHIP = \
pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = \
pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = \
pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))

# Player ship
YELLOW_SPACE_SHIP = \
pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(
    pygame.image.load(os.path.join("assets","background-black.png")), # image 
    (WIDTH, HEIGHT) # new size
)

world_state = {
            'Player': None,
            'Enemies': [],
            'PlayerLasers': [],
            'EnemyLasers': []
        }

## START CLASS DEFINITIONS

class Actions:   
    @staticmethod
    def collision(obj1, obj2):
        '''Detect collision between two objects'''
        offset_x = obj1.x - obj2.x
        offset_y = obj1.y - obj2.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
    
    @staticmethod
    def move(obj, velocity, direction):
        '''Move an object up down left or right with certain velocity'''
        if direction == 'up':
            obj.y -= velocity
        elif direction == 'down':
            obj.y += velocity
        elif direction == 'left':
            obj.x -= velocity
        elif direction == 'right':
            obj.x += velocity
        else:
            pass

    @staticmethod
    def offscreen_x(obj, width):
        '''Determine if obj is offscreen in the x direction'''
        return obj.x > width or obj.x < 0

    @staticmethod
    def offscreen_y(obj, height):
        '''Determine if obj is offscreen in the y direction'''
        return obj.y > height 

    @staticmethod
    def is_offscreen(obj, width, height):
        '''Determine if obj is offscreen in either direction'''
        return Actions.offscreen_x(obj, width) or Actions.offscreen_y(obj,
                                                                      height
                                                                     ) 
    @staticmethod
    def make_wave():
        pass

class Ship:
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.cooldown_counter = 0
        self.cooldown_limit = 30

    def draw(self, window):
        '''Draw the ship_img at ship's current position (x, y)'''
        window.blit(self.ship_img, (self.x, self.y))

    def width(self):
        '''Get the ship's width'''
        return self.ship_img.get_width()

    def height(self):
        '''Get the ship's height'''
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cooldown_counter < self.cooldown_limit:
            self.cooldown_counter += 1
            return False
        elif self.cooldown_counter >= self.cooldown_limit:
            self.cooldown_counter = 0
            return True


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.cooldown_counter = 0
        self.cooldown_limit = 20

    def health_bar(self, window):
        pygame.draw.rect(
            window, 
            (255,0,0), # red 
            (self.x, self.y + self.ship_img.get_height() + 10, \
             self.ship_img.get_width(), 10)
        )

        curr_health_pct = self.health / 100

        pygame.draw.rect(
            window, 
            (0,255,0), # green 
            (self.x, self.y + self.ship_img.get_height() + 10, \
             self.ship_img.get_width() * curr_health_pct, 10)
        )

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)
    
    def shoot(self):
        '''Fire a laser fof = 'PlayerLaser' or 'EnemyLaser' '''
        if self.cooldown():
            laser = Laser(self.x, self.y, self.laser_img)
            world_state['PlayerLasers'].append(laser)
            self.cooldown_counter = 1
        else:
            pass

class Enemy(Ship):
    COLOR_MAP = {
        'red': (RED_SPACE_SHIP, RED_LASER),
        'green': (GREEN_SPACE_SHIP, GREEN_LASER),
        'blue': (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, health=1):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = Enemy.COLOR_MAP[random.choice(['red','green','blue'])]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.cooldown_counter = 0
        self.cooldown_limit = 20
    
    def shoot(self):
        '''Fire a laser fof = 'PlayerLaser' or 'EnemyLaser' '''
        if self.cooldown():
            laser = Laser(self.x, self.y, self.laser_img)
            world_state['EnemyLasers'].append(laser)
            self.cooldown_counter = 1
        else:
            pass

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

## END CLASS DEFINITIONS

def main(): 
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    level = 0 
    lives = 5
    main_font = pygame.font.SysFont("arial", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    player_vel = 5
    lost = False
    lost_count = 0
    world_state['Player'] = Player(300, 530)
    wave_length = 5
    enemy_vel = 1
    laser_velocity = 10

    def redraw_window():
        WIN.blit(BG, (0,0)) # Draw background
        
        # Draw text
        lives_label = main_font.render(f"Lives: {lives} ", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level} ", 1, (255,255,255))
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        
        # Draw enemies
        for enemy in world_state['Enemies']:
            enemy.draw(WIN)

        # Draw player
        world_state['Player'].draw(WIN)
        
        # Draw enemy lasers
        for laser in world_state['EnemyLasers']:
            laser.draw(WIN)

        # Draw player lasers
        for laser in world_state['PlayerLasers']:
            laser.draw(WIN)

        if lost:
            lost_label = lost_font.render("You lost!!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 250))

    while run:
        # Game Loop
        clock.tick(FPS)
        redraw_window()
        
        # Game over test and counter
        if lives <= 0 or world_state['Player'].health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3: # wait 3 seconds
                run = False
            else:
                pass

        pygame.display.update()

        # New wave of enemies
        if len(world_state['Enemies']) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(
                    random.randrange(50, WIDTH - 100),
                    random.randrange(-1500, -100)
                    )
                world_state['Enemies'].append(enemy)

        # Check for user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            else:
                pass

        # Read inputs and move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and ((world_state['Player'].x - player_vel) > 0): # left
            Actions.move(world_state['Player'], player_vel, 'left')
        if keys[pygame.K_d] and ((world_state['Player'].x + player_vel + world_state['Player'].width()) < WIDTH): # right
            Actions.move(world_state['Player'], player_vel, 'right')
        if keys[pygame.K_w] and ((world_state['Player'].y - player_vel) > 0): # up
            Actions.move(world_state['Player'], player_vel, 'up')
        if keys[pygame.K_s] and ((world_state['Player'].y + player_vel + world_state['Player'].height()) + 10 < HEIGHT):
            Actions.move(world_state['Player'], player_vel, 'down')
        if keys[pygame.K_SPACE]:
            world_state['Player'].shoot()

        world_state['Player'].cooldown()

        # Move enemies and let them shoot 
        for enemy in world_state['Enemies'][:]:
            Actions.move(enemy, enemy_vel, 'down')
            enemy.cooldown()
            if random.randrange(0, 120) == 1:
                enemy.shoot()
            if Actions.collision(world_state['Player'], enemy):
                world_state['Player'].health -= 10
                world_state['Enemies'].remove(enemy)
            elif enemy.y + enemy.height() > HEIGHT:
                lives -= 1
                world_state['Enemies'].remove(enemy)
        
        # Move Player lasers
        for laser in world_state['PlayerLasers'][:]:
            Actions.move(laser, laser_velocity, 'up')
            for enemy in world_state['Enemies'][:]:
                if Actions.collision(laser, enemy):
                    # world_state['PlayerLasers'].remove(laser)
                    world_state['Enemies'].remove(enemy)
                elif laser.y <= 0:
                    # world_state['PlayerLasers'].remove(laser)
                    pass

        # Move Enemy lasers
        for laser in world_state['EnemyLasers'][:]:
            Actions.move(laser, laser_velocity, 'down')
            if Actions.collision(laser, world_state['Player']):
                world_state['Player'].health -= 10
                world_state['EnemyLasers'].remove(laser)
            elif laser.y >= HEIGHT:
                world_state['EnemyLasers'].remove(laser)
    
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render(
            "Press the mouse button to begin", 
            1,
            (255,255,255)
        )

        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
