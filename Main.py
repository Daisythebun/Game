
# Setup Python ----------------------------------------------- #
import pygame
import sys
import random


# Setup pygame/window ---------------------------------------- #
pygame.init()
pygame.display.set_caption('Space shooter')
SCREEN_WIDTH = 500
SCREEN_HEIGHT= 680
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)

mainClock = pygame.time.Clock()

# Fonts ------------------------------------------------------- #
main_font = pygame.font.SysFont("Californian FB", 42) # to be able to write
big_font = pygame.font.SysFont("Californian FB", 62)

# Variables ------------------------------------------------------- #
enemy_list = [] # will store the enemy
enemy_spawn_time = 1 # every x seconds a enemy will spawn
enemy_spawn_timer = 0 # timer for making spawn enemy

# Constantes -------------------------------------------------------#
START_TIME = pygame.time.get_ticks()

STARS = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(2, 4)) for i in range(100)] # stars posx, posy, radius

BG_COLOR = (22,22,28)

# Classes --------------------------------------------------------- #
class Player:
    def __init__(self):
        size = (32, 48) # size of the player
        self.sprite = pygame.transform.scale(pygame.image.load("Sprites/ship_0.png"), size) # load and scale the player sprite
        bullet_size = (9, 22) #size of the bullet
        self.bullet_sprite = pygame.transform.scale(pygame.image.load("Sprites/player_bullet.png"), bullet_size) # load and scale the bullet sprite

        self.spawn_pos_x = SCREEN_WIDTH//2 # the player x start pos

        self.rect = pygame.Rect(self.spawn_pos_x, 0, self.sprite.get_width(), self.sprite.get_height()) # rect object that store x, y pos and width, height of the player

        self.turn_speed = 3 # how fast he can turn right or left

        self.reload_time = 0.5 # time that the player take to reload (in seconds)
        self.shoot_timer = 0 # timer that keep track of when the player has shoot
        self.bullet_pos_list = [] # list that will contain all bullets position
        self.bullet_speed = 3


        self.life = 0
        self.score = 0


    def reset(self): # reset all variables
        self.score = 0 # how many enemy the player has killed
        self.life = 3 # how many live the player have
        self.rect.y =  SCREEN_HEIGHT - self.sprite.get_height() - 40 # y pos of the player


    def move(self): # make the player move
        vel = 0
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            vel -= self.turn_speed

        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            vel += self.turn_speed

        self.rect.x += vel # make the player move
        # make that the player can't go outside the screen
        if self.rect.x < 0: # at the left
            self.rect.x = 0
        if self.rect.right > SCREEN_WIDTH: # at the right
            self.rect.right = SCREEN_WIDTH


    def shoot(self): # make the player shoot a new bullet if he has reloaded
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE] and self.shoot_timer < time:
            self.shoot_timer = time + self.reload_time
            self.bullet_pos_list.append([self.rect.centerx - self.bullet_sprite.get_width()//2, self.rect.y]) # create a new bullet at the player location


    def move_bullets(self, bullet): # move and remove the bullet if outside the screen
        bullet[1] -= self.bullet_speed
        if bullet[1] + self.bullet_sprite.get_height() < 0:
            self.bullet_pos_list.remove(bullet)


    def draw_bullets(self, bullet): # draw the bullet that the player shoot
        SCREEN.blit(self.bullet_sprite, bullet)


    def make_bullets(self): # handle bullets
        self.shoot()
        for bullet in self.bullet_pos_list:
            self.move_bullets(bullet)
            self.draw_bullets(bullet)


    def draw_infos(self): # draw life and kill of the player
        life_label = main_font.render(f"Lives : {self.life}", 1, (33, 188, 111))
        SCREEN.blit(life_label, (SCREEN_WIDTH-life_label.get_width()-5, 5))
        kill_label = main_font.render(f"Kills : {self.score}", 1, (200, 144, 55))
        SCREEN.blit(kill_label, (SCREEN_WIDTH-kill_label.get_width()-5, 10 + life_label.get_height()))


    def draw(self): # draw the player
        SCREEN.blit(self.sprite, self.rect)
        self.draw_infos()



class Enemy:
    def __init__(self):
        self.size_mult = random.uniform(0.7, 2.4) # how many the image will be scale (ex : 2 -> 2 time bigger image)
        self.enemy_sprite = pygame.transform.scale(pygame.image.load("Sprites/enemy_ship.png"), (int(32*self.size_mult), int(16*self.size_mult)))
        self.x_pos = random.randint(0, int(SCREEN_WIDTH-self.enemy_sprite.get_width()))

        self.rect = pygame.Rect(self.x_pos, 0-self.enemy_sprite.get_height(), self.enemy_sprite.get_width(), self.enemy_sprite.get_height())  # store the pos and size of the enemy

        self.y_vel = random.uniform(1.5, 3) # speed of the enemy

        bullet_size = int(4 + self.size_mult*4)
        self.bullet_sprite = pygame.transform.scale(pygame.image.load("Sprites/enemy_bullet.png"), (bullet_size, bullet_size))
        self.reload_time = 3 # time that the enemy take to reload (in seconds)
        self.shoot_timer = 0 # timer that keep track of when the enemy has shoot
        self.bullet_pos_list = [] # list that will contain all bullets position
        self.bullet_speed = self.y_vel * 2 # speed of the bullet


    def move(self):
        self.rect.y += self.y_vel
        if self.rect.y > SCREEN_HEIGHT:
            return "out_of_screen"


    def collide(self): # collision with the player
        if self.rect.colliderect(player.rect):
            player.life -= 1
            return "collide_player"


    def bullet_collide(self): # make collide the bullet that the player have shooted with the enemy
        for bullet in player.bullet_pos_list:
            if self.rect.right > bullet[0] > self.rect.left:
                if self.rect.bottom > bullet[1] > self.rect.top:
                    player.score +=1
                    return "bullet_hit_enemy"


    def draw(self):
        SCREEN.blit(self.enemy_sprite, self.rect)

# Creation ---------------------------------------------------------#
player = Player()

enemy_list.append(Enemy())


def reset_game():
    if player.score > 0:
        kill_label = main_font.render(f"You killed : {player.score} spaceships!", 1, (200, 144, 55)) # score text
        SCREEN.blit(kill_label, (SCREEN_WIDTH//2-kill_label.get_width()//2, SCREEN_HEIGHT//3))

    start_label = main_font.render(f"Press R to Start a game", 1, (33, 188, 111)) # start game text
    SCREEN.blit(start_label, (SCREEN_WIDTH//2-start_label.get_width()//2, SCREEN_HEIGHT//2))

    enemy_list.clear() # remove all the enemy


def redraw(): # make the game work (draw on screen,..)
    global enemy_spawn_timer
    SCREEN.fill(BG_COLOR)
    

    if player.life > 0:
        player.make_bullets()
        player.draw()
        player.move()


        if time > enemy_spawn_timer: # spawn a new enemy
            enemy_list.append(Enemy())
            enemy_spawn_timer = time +enemy_spawn_time

        for enemy in enemy_list:
            if enemy.move() == "out_of_screen":
                enemy_list.remove(enemy)
                continue

            if enemy.collide() == "collide_player": # remove the enemy after collision
                enemy_list.remove(enemy)
                continue

            if enemy.bullet_collide() == "bullet_hit_enemy": # remove the enemy bullet after collision
                enemy_list.remove(enemy)
                continue

            

            enemy.draw()

    elif player.life <= 0:
        reset_game()



def buttons(): # user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r and player.life <= 0:
                player.reset()


def update(): # update all the screen
    pygame.display.update()
    mainClock.tick(90) # make the game run at 90 frame / sec


# Loop ------------------------------------------------------- #
while True:

    time = (pygame.time.get_ticks() - START_TIME)/1000 # time

    # draw --------------------------------------------- #
    redraw()

    # Buttons ------------------------------------------------ #
    buttons()

    # Update ------------------------------------------------- #
    update()
