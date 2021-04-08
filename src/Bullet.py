import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        self.speed = 0
        self.group = pygame.sprite.Group()
        pygame.sprite.Sprite.__init__(self, self.group)
