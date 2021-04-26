import pygame
import pygame.locals
import data.settings





class Door(pygame.sprite.Sprite):
    def __init__(self, x_coordinate, y_coordinate):
        super().__init__()
        # Door is represented as a robot for the time being.
        img = pygame.image.load('./img/robo.png')
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
        # self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate


class Rock(pygame.sprite.Sprite):
    def __init__(self, x_coordinate, y_coordinate, direction):
        super().__init__()
        img = pygame.image.load('./img/rock.png')
        self.image = pygame.transform.scale(img, (20, 20))
        # self.image.convert_alpha()
        # self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (x_coordinate, y_coordinate)
        self.speed = 10
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > data.settings.SCREEN_WIDTH:
            self.kill()
