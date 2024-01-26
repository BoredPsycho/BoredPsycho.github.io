import pygame
from sys import exit
import random as rand

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emma's hardcore race")

background = pygame.transform.scale(pygame.image.load('Emma/map_asset.jpg').convert(),(WIDTH, HEIGHT))
explosion_image = pygame.transform.scale(pygame.image.load('Emma/single_explosion.png'),(150,150))

game_font = pygame.font.SysFont("NSimSun", 80)
GRAY = (100, 100, 100)
EXPLOSION = pygame.mixer.Sound('Emma/Grenade+1.mp3')
kills = []

def bottom():
    kill_count = game_font.render(f"{len(kills)} cars crashed!", False, (230,230,230))
    kill_count_rect = kill_count.get_rect(bottomright = (WIDTH - 10, HEIGHT))
    emma_face1 = pygame.transform.scale(pygame.image.load('Emma/emma.jpg').convert(), (100,100))
    emma_face1_rect = emma_face1.get_rect(bottomleft = (10, HEIGHT))
    velocimetro = game_font.render(f"{player.vel * 10} Km/h", False, (250,50,50))
    velocimetro_rect = velocimetro.get_rect(bottomleft = (150, HEIGHT))
    bottom_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 200)
    pygame.draw.rect(window, GRAY, bottom_rect)
    window.blit(emma_face1, emma_face1_rect)
    window.blit(kill_count,kill_count_rect)
    window.blit(velocimetro, velocimetro_rect)

def expimg(x,y):
    image = explosion_image
    rect = image.get_rect(center = (x,y))
    window.blit(image,rect)

class Player():
    def __init__(self):
        self.image = pygame.transform.rotozoom(pygame.image.load('Emma/player/12.png'), 90, 1.1)
        self.image_static = pygame.transform.rotozoom(pygame.image.load('Emma/player/12.png'), 90, 1.1)
        self.image_left = pygame.transform.rotate(self.image, 45)
        self.image_right = pygame.transform.rotate(self.image, 135)
        self.rect = self.image.get_rect(center = (WIDTH//2, HEIGHT//2))
        self.vel = 8
        self.armor = False
    
    def player_draw(self):
        window.blit(self.image, self.rect)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 0:
            self.image = self.image_static
            self.rect.y -= self.vel
        if keys[pygame.K_s] and self.rect.y < HEIGHT - 215:
            self.image = self.image_static
            self.rect.y += self.vel
        if keys[pygame.K_d] and self.rect.x < WIDTH - 120:
            self.image = self.image_right
            self.rect.x += self.vel
        if keys[pygame.K_a] and self.rect.x > 0:
            self.image = self.image_left
            self.rect.x -= self.vel
    
    def update(self):
        self.player_draw()
        self.player_input()

class Enemy():
    def __init__(self):
        self.image = enemy_image[rand.randint(0,4)]
        self.rect = self.image.get_rect(center = (rand.randint(100, 900), -200))
        self.vel = 6
        self.ori = rand.randint(0,1)
    def update(self):
        self.rect.y += self.vel
        if self.ori == 0:
            self.rect.x += self.vel
            if self.rect.x > WIDTH - 100:
                self.ori = 1
        if self.ori == 1:
            self.rect.x -= self.vel
            if self.rect.x <= 100:
                self.ori = 0
        window.blit(self.image,self.rect)
        if self.rect.y > HEIGHT:
            enemy_list.remove(self)
        if self.rect.colliderect(player.rect):
            expimg(self.rect.x, self.rect.y)
            enemy_list.remove(self)
            kills.append(1)
            EXPLOSION.play()

class Obstacle():
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('Emma/mine.png'), (50,50))
        self.rect = self.image.get_rect(center = (rand.randint(100, 900), -200))
    def update(self):
        self.rect.y += 10
        window.blit(self.image,self.rect)
        if self.rect.y > HEIGHT:
            obstacle_list.remove(self)

    def game_over(self):
        if self.rect.colliderect(player.rect):
            obstacle_list.remove(self)
            EXPLOSION.play()
            return False
        else:
            return True
        
    def game_over_2(self):
        if self.rect.colliderect(player.rect):
            return True
        else:
            return False
        
class Power():
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('Emma/old_lady.png'), (50,50))
        self.rect = self.image.get_rect(bottomleft = (-200, rand.randint(210, 500)))
    def update(self):
        self.rect.x += 4
        window.blit(self.image,self.rect)
        if self.rect.x > WIDTH:
            power_list.remove(self)
        if self.rect.colliderect(player.rect):
            player.vel += 1
            power_list.remove(self)

player = Player()

enemy_list = []
obstacle_list = []
power_list = []
enemy_image = [pygame.transform.rotozoom(pygame.image.load('Emma/cars/1.png'), 270, 1.1),
               pygame.transform.rotozoom(pygame.image.load('Emma/cars/2.png'), 270, 1.1),
               pygame.transform.rotozoom(pygame.image.load('Emma/cars/3.png'), 270, 1.1),
               pygame.transform.rotozoom(pygame.image.load('Emma/cars/4.png'), 270, 1.1),
               pygame.transform.rotozoom(pygame.image.load('Emma/cars/5.png'), 270, 1.1)]

clock = pygame.time.Clock()
enemy_timer = pygame.USEREVENT + 1
obstacle_timer = pygame.USEREVENT + 2
power_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy_timer, 1000)
pygame.time.set_timer(obstacle_timer, 1500)
pygame.time.set_timer(power_timer, 5000)
game_active = False
death = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if game_active:
        window.blit(background, (0,0))

        if event.type == obstacle_timer and len(obstacle_list) < 12:
            obstacle_list.append(Obstacle())
        for obstacle in obstacle_list:
            Obstacle.update(self=obstacle)
            game_active = Obstacle.game_over(self=obstacle)
            death = Obstacle.game_over_2(self=obstacle)

        if event.type == enemy_timer and len(enemy_list) < 5:
            enemy_list.append(Enemy())
        for enemy in enemy_list:
            Enemy.update(self=enemy)

        if event.type == power_timer and len(power_list) < 2:
            power_list.append(Power())
        for power in power_list:
            Power.update(self=power)

        player.update()

        bottom()
    else:
        window.fill(GRAY)
        if death:
            intro_msg = game_font.render("YOU GOT RECKED!!!",
                                      False, (230,230,230))
            player.vel = 8
            enemy_list.clear()
            obstacle_list.clear()
            power_list.clear()
            kills.clear()
        else:
            intro_msg = game_font.render("GO GET THEM!!!",
                                      False, (230,230,230))
        command_msg = game_font.render("PRESS WASD TO RUN THEM OVER",
                                      False, (230,230,230))
        intro_msg_rect = intro_msg.get_rect(center = (WIDTH//2, HEIGHT//2 - 100))
        command_msg_rect = command_msg.get_rect(center = (WIDTH//2, HEIGHT//2 + 100))
        window.blit(intro_msg, intro_msg_rect)
        window.blit(command_msg, command_msg_rect)
        if pygame.key.get_pressed()[pygame.K_w]:
            game_active = True
            death = False

    pygame.display.update()
    clock.tick(60)