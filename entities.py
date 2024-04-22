import pygame
import random
import os

IMAGE_PATH = "res/Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.image.load(os.path.join(IMAGE_PATH, img)).convert_alpha() for img in PLAYER_IMAGES]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image_index = 0

    def change_image(self):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index]

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('res/enemy.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 35))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.move_speed = random.randint(-6, -4)

    def move(self):
        self.rect.x += self.move_speed

class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('res/bonus.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 150))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.move_speed = random.randint(4, 6)

    def move(self):
        self.rect.y += self.move_speed
