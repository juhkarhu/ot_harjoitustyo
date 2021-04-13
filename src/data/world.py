import pygame
import data.SETTINGS


'''
This class is for generic world object such doors and ground tiles. 
'''

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Door is represented as a robot for the time being. 
        img = pygame.image.load('./img/robo.png')
        self.image = pygame.transform.scale(img, (data.SETTINGS.TILE_SIZE, data.SETTINGS.TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (data.SETTINGS.TILE_SIZE, data.SETTINGS.TILE_SIZE))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        img = pygame.image.load('./img/rock.png')
        self.image = pygame.transform.scale(img, (20, 20))
        # self.image.convert_alpha()
        # self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > data.SETTINGS.SCREEN_WIDTH:
            self.kill()