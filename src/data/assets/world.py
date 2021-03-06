import pygame
import pygame.locals
import data.settings

'''
World objects are created from the classes shown here.
'''


class Door(pygame.sprite.Sprite):
    def __init__(self, x_coordinate, y_coordinate):
        super().__init__()
        img = pygame.image.load('./img/ovi.png')
        self.image = pygame.transform.scale(
            img, (data.settings.TILE_SIZE, data.settings.TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate


class Tile(pygame.sprite.Sprite):
    def __init__(self, x_coordinate, y_coordinate, image):
        super().__init__()
        self.image = pygame.transform.scale(
            image, (data.settings.TILE_SIZE, data.settings.TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate


class Rock(pygame.sprite.Sprite):
    def __init__(self, x_coordinate, y_coordinate, direction):
        super().__init__()
        img = pygame.image.load('./img/rock.png')
        self.image = pygame.transform.scale(img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x_coordinate, y_coordinate)
        self.speed = 10
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > data.settings.SCREEN_WIDTH:
            self.kill()
