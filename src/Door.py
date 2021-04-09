import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        # Door is represented as a robot for the time being. 
        img = pygame.image.load('./img/robo.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        