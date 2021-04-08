import pygame
from SETTINGS import *
import os
from Game import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, character_type, x, y, scale, speed, id):
        super().__init__()
        self.direction = 1
        self.alive = True
        self.character_type = character_type
        self.speed = speed
        self.jumped = False
        self.move_counter = 0
        self.vision = pygame.Rect(0,0,100, 10)

        self.climbheight = 4
        self.dig = False
        self.action = 0
        self.frame_index = 0
        self.in_air = True
        self.velocity_y = 0
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        self.bullet_image = pygame.image.load('./img/icons/bullet.png')
        animation_types = ['idle', 'run', 'jump']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'img/{self.character_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.character_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        # self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (x, y)


    def draw(self, screen):
        self.update_animation()
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)

    def ai(self, map):
        if self.alive:
            self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
            if self.direction == 1:
                ai_moving_right = True
            else:
                ai_moving_right = False
            ai_moving_left = not ai_moving_right
            self.update(map, ai_moving_left, ai_moving_right)
            self.move_counter += 1

            if self.move_counter > 2*SCALA:
                self.direction *= -1
                self.move_counter = 0

    def update(self, map, left, right):
            if self.in_air: # Jumping or falling
                self.update_action(2)

            self.update_action(1)
            movement_x = 0
            movement_y = 0

            # Flip the sprite depending where it's facing
            if self.direction < 0:
                self.flip = True
            else:
                self.flip = False

            # Move the charaxter on X-axis
            self.rect.x += (1 * self.direction)
            # Add Gravity to the velocity that the object is falling
            self.velocity_y += GRAVITY
            
            # Move the charaxter on Y-axis
            movement_y += self.velocity_y
            
            # check for collision
            for tile in map:
                # Check is characters collide with wall to their left and turn them as needed.
                if tile[1].colliderect(self.rect.x + movement_x, self.rect.y, self.rect.width, self.rect.height):               
                    self.direction *= -1
                    self.rect.x += self.direction
                    movement_x = 0
                # Check whether there is ground below characters feet
                if tile[1].colliderect(self.rect.x, self.rect.y + movement_y, self.rect.width, self.rect.height):
                    self.in_air = False
                    if self.velocity_y < 0:
                        movement_y = tile[1].bottom - self.rect.top
                    elif self.velocity_y >= 0:
                        movement_y = tile[1].top - self.rect.bottom
                        self.velocity_y = 0
                
                    
            self.rect.x += movement_x
            self.rect.y += movement_y


    def update_animation(self):
        # Update animation        
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()