import pygame

#tile = (img, img_rect)
class Tile(pygame.sprite.Sprite):
    def __init__(self, img ,img_rect):
        super().__init__()
        self.img = img
        self.rect = img_rect
        self.mask = pygame.mask.from_surface(self.img)