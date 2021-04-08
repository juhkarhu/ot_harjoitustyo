import pygame
from SETTINGS import *
import os
from Game import *

class Player(pygame.sprite.Sprite):
    def __init__(self, character_type, x, y, scale, speed, id):
        super().__init__()
        self.id = id
        self.direction = 1
        self.alive = True
        self.character_type = character_type
        self.speed = speed
        self.jumped = False

        # import os.path
        # path = f'{os.getcwd()}/img/{self.character_type}/{animation}'
        # num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
        # print(num_files)

        # Defines if character can climb the obstacle in front of it automatically
        self.climbheight = 4
        self.player_controlled = False
        self.dig = False
        self.action = 0
        self.frame_index = 0
        self.in_air = True
        self.velocity_y = 0
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        self.bullet_image = pygame.image.load('./img/icons/bullet.png').convert_alpha()
        animation_types = ['idle', 'run', 'jump']
        for animation in animation_types:
            temp_list = []
            # Ei toiminut laitoksen koneella.
            # num_of_frames = len(os.listdir(f'img/{self.character_type}/{animation}'))

            # Hakee ensin sovelluksen sijainnin ja sitten tutkii kansiot. 
            path = f'{os.getcwd()}/img/{self.character_type}/{animation}'
            num_of_frames = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])

            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.character_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        # self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (x, y)

    def get_animation_list(self):
        return len(self.animation_list)

    def get_id(self):
        return self.id

    def take_control(self):
        # self.kill()
        self.player_controlled ^= True

    # def give_control(self):
    #     self.player_controlled = False

    def update(self, map, left, right):
        if self.in_air: # Jumping or falling
            self.update_action(2)
        elif left or right: # Walking by player
            self.update_action(1)
        elif not self.player_controlled: # Walking automatically
            self.update_action(1)
        else:
            self.update_action(0)
        movement_x = 0
        movement_y = 0

        # Lemming is being controlled by the player
        if self.player_controlled:
            key = pygame.key.get_pressed()

            if key[pygame.K_w] and self.jumped == False and self.in_air == False:
                self.velocity_y = -13
                self.jumped = True
                self.in_air = True
            if key[pygame.K_w] == False:
                self.jumped = False

            
            # Movement to the left
            if left:
                movement_x = -self.speed
                self.flip = True
                self.direction = -1
            # Movement to the right
            if right:
                movement_x = self.speed
                self.flip = False
                self.direction = 1

            
        # Lemming is not being controlled by the player
        else:
            if self.direction < 0:
                self.flip = True
            else:
                self.flip = False
            self.rect.x += (1 * self.direction)
        self.velocity_y += GRAVITY
                        
        # One can fall regardless of being controlled or not
        # if self.velocity_y > 10:
        #     self.velocity_y = 10        
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
    

    def draw(self, screen):
        self.update_animation()
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)


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
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    # This is not needed anymore, I think..
    def ground_at_position(self, pos, map):
        if map[pos[1]][pos[0]] != 0:
            return True
        else:
            return False