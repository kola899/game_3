import pygame
import os
import sys
import random

pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1200
HEIGHT = 800
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
from load import *

def restart():
    global player_group, food_group, enemy1_group, enemy2_group
    player_group = pygame.sprite.Group()
    food_group = pygame.sprite.Group()
    enemy1_group = pygame.sprite.Group()
    enemy2_group = pygame.sprite.Group()
    player = Player(player_image, (100, 100))
    player_group.add(player)

def game_lvl():
    sc.fill('gray')
    food_group.update()
    food_group.draw(sc)
    player_group.update()
    player_group.draw(sc)
    enemy1_group.update()
    enemy1_group.draw(sc)
    enemy2_group.update()
    enemy2_group.draw(sc)
    pygame.display.update()

class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = food_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)



class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.key = pygame.key.get_pressed()
        self.speed = 10
        self.pos = self.rect.center


    def eat(self):
        if pygame.sprite.spritecollide(self, food_group, True):
            self.image = pygame.transform.rotozoom(self.image, 0, 1.05)
            self.pos = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
        if pygame.sprite.spritecollide(self, enemy1_group, False):
            enemy = pygame.sprite.spritecollide(self, enemy1_group, False)[0]
            if enemy.image.get_height() <= self.image.get_height():
                enemy.kill()
                self.pos = self.rect.center
                self.image = pygame.transform.rotozoom(self.image, 0, 1.05)
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
    def update(self):
        self.move()
        self.eat()
        self.key = pygame.key.get_pressed()



    def move(self):
        if self.key[pygame.K_d] and self.rect.right < WIDTH: #Мини-барьер
            self.rect.x += self.speed
        elif self.key[pygame.K_a] and self.rect.left > 0:
                self.rect.x -= self.speed

        elif self.key[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed

        elif self.key[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = self.rect.center
        self.timer_move = 0
        self.speed_x = random.randint(-5, 5)
        self.speed_y = random.randint(-5, 5)


    def update(self):
        self.timer_move += 1
        if self.timer_move / FPS > 3:
            self.speed_x = random.randint(-5, 5)
            self.speed_y = random.randint(-5, 5)
            self.timer_move = 0
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

class Spawn():
    def __int__(self):
        self.timer = 0

    def update(self):
        if len(food_group) < 20:
            food = Food()
            food_group.add(food)
        if len(enemy1_group) < 5:
            pos = (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))




restart()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    game_lvl()
    clock.tick(FPS)