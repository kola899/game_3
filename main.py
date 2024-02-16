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
    global player_group, food_group, enemy1_group, enemy2_group, spawner, eyes_group
    player_group = pygame.sprite.Group()
    food_group = pygame.sprite.Group()
    enemy1_group = pygame.sprite.Group()
    enemy2_group = pygame.sprite.Group()
    player = Player(player_image, (100, 100))
    player_group.add(player)
    spawner = Spawn()
    eyes_group = pygame.sprite.Group()


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
    spawner.update()

    eyes_group.update()
    eyes_group.draw(sc)
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
        if self.key[pygame.K_d] and self.rect.right < WIDTH:  # Мини-барьер
            self.rect.x += self.speed
        elif self.key[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed

        elif self.key[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed

        elif self.key[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


class Enemy1(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = self.rect.center
        self.timer_move = 0
        self.speed_x = random.randint(-5, 5)
        self.speed_y = random.randint(-5, 5)
        self.food = None
        self.agr = False


    def update(self):
        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_x *= -1
            self.speed_y *= -1
        self.timer_move += 1
        if self.timer_move / FPS > 3:
            self.speed_x = random.randint(-5, 5)
            self.speed_y = random.randint(-5, 5)
            self.timer_move = 0
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if pygame.sprite.spritecollide(self,food_group, True):
            self.pos = self.image = self.rect.center
            self.image = pygame.transform.rotozoom(self.image, 0, 1.05)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos


            self.eyes.pos = self.rect.center
            self.eyes.image = pygame.transform.rotozoom(self.eyes, 0, 1.05)
            self.eyes.rect = self.eyes.image.get_rect()
            self.eyes.rect.center = self.eyes.pos
            self.agr = False



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



class Enemy2(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = self.rect.center
        self.timer_move = 0
        self.speed_x = random.randint(-5, 5)
        self.speed_y = random.randint(-5, 5)
        self.food = None
        self.agr = False


    def update(self):
        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_x *= -1
            self.speed_y *= -1
        self.timer_move += 1
        if self.timer_move / FPS > 3:
            self.speed_x = random.randint(-5, 5)
            self.speed_y = random.randint(-5, 5)
            self.timer_move = 0
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.timer_move / FPS > 3 and self.agr == False:
            self.speed_x = random.randint(-1, 1)
            self.speed_Y = random.randint(-1, 1)
            self.timer_move = 0
        if self.agr:
            if self.rect.center[0] > self.food.rect.center[0]:
                self.speed_x = -1
                if self.rect.center[1] > self.food.rect.center[1]:
                    self.speed_Y = -1
                else:
                    self.speed_Y = 1
            else:
                self.speed_x = 1
                if self.rect.center[1] > self.food.rect.center[1]:
                    self.speed_Y = -1
                else:
                    self.speed_Y = 1



class Eyes(pygame.sprite.Sprite):
    def __init__(self, pos, block, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = eyes_image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.block = block
        self.type = type
        self.pos = pos


    def update(self):
        self.rect.center = self.block.rect.center
        if self.type == 1:
            if (
                    pygame.sprite.spritecollide(self, food_group, False)
                    and self.block.agr == True
            ):
                food = pygame.sprite.spritecollide(self, food_group, False)[0]
                self.block.agr = True
                self.block.food = food
                self.timer_move = 0




class Spawn():
    def __int__(self):
        self.timer = 0

    def update(self):
        if len(food_group) < 20:
            food = Food()
            food_group.add(food)
        if len(enemy1_group) < 5:
            pos = (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))
            enemy = Enemy1(enemy1_image, pos)
            eyes = Eyes(enemy.rect.center, enemy, 1)
            enemy.eyes = eyes
            eyes_group.add(eyes)
            enemy1_group.add(enemy)
        if len(enemy2_group) < 5:

            pos = (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))
            enemy = Enemy2(enemy2_image, pos)
            eyes = Eyes(enemy.rect.center, enemy, 1)
            enemy.eyes = eyes
            eyes_group.add(eyes)
            enemy2_group.add(enemy)







restart()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    game_lvl()
    clock.tick(FPS)
