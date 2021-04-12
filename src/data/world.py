import pygame
from data.SETTINGS import *


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Door is represented as a robot for the time being. 
        img = pygame.image.load('./img/robo.png')
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y