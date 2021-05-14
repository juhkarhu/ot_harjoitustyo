'''
Handles the character logic for player and enemy characters.
'''

import os
import pygame
import data.settings
from datetime import datetime



class Lemminki(pygame.sprite.Sprite): #pylint: disable=too-many-instance-attributes
    # Disabled error message from standard pygame class
    '''
    Initialization of the class.
    '''
    def __init__(self, character_type, scale, starting_pos, id_number):
        super().__init__()

        self.id_number = id_number
        self.move_counter = 0
        self.throw_cooldown = 0
        self.control = False
        self.speed = 2
        self.moving_right = False
        self.moving_left = False
        self.player_y_momentum = 0
        self.player_x_momentum = 0
        self.air_timer = 0
        self.direction = 1
        self.in_air = False
        self.flip = False
        self.thrown_rocks = pygame.sprite.Group()
        self.conscious = True
        self.cooldown_tracker = 0

        self.hitpoints = 3
        self.invincible = True
        self.last_collide = 0
        self.current_time = pygame.time.get_ticks()

        # These are defined as None for the sake of pylint
        # They are used elsewhere.
        self.action = None
        self.frame_index = None
        self.update_time = None
        self.image = None
        self.player_movement = None
        self.collision_types = None
        self.hit_list = None

        # The normal init continues from here:
        self.load_images(character_type, scale, starting_pos)

    def load_images(self, character_type, scale, starting_pos):
        '''
        Loads all the images used for the character sprites.
        All the animations have the same image as placeholder. Easy enough to edit if time allows.
        '''
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        animation_types = ['attack', 'death', 'idle', 'jump', 'run']
        for animation in animation_types:
            temp_list = []
            path = f'{os.getcwd()}/img/{character_type}/{animation}'
            num_of_frames = len([f for f in os.listdir(
                path)if os.path.isfile(os.path.join(path, f))])
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{character_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (starting_pos)



    def get_id(self):
        '''
        Returns the object id. Used for checking if the
        player can take control of the clicked character.
        '''
        return self.id_number

    def take_control(self):
        '''
        Alters the self.control to true so that the player can control the character.
        '''
        self.control = True

    def give_control(self):
        '''
        Alters the self.control to false so that the player can't control the character.
        '''
        self.control = False

    def get_hit_player(self):
        if not self.immune():
            self.hitpoints -= 1
            self.last_collide = pygame.time.get_ticks()
        if self.hitpoints == 0:
            return True

    def get_hitpoints(self):
        return self.hitpoints

    def immune(self):
        return self.last_collide > pygame.time.get_ticks() - 3000

    def get_conscious_state(self):
        return self.conscious

    def get_hit_enemy(self):
        '''
        Handles the hit detection for enemy class.
        The enemy will go unconscious for a few seconds and then come back to being awake.
        '''
        if self.conscious:
            self.conscious = False
            self.update_action(1)
            self.update_animation()


    def ai_movement(self, display, tile_rects, left, right, jump, shoot):
        '''
        AI controls the NPC characters and makes them walk for the
        length of two tiles with the help of update().
        '''

        if not self.conscious:
            self.update_action(1)
            self.update_animation()
            self.cooldown_tracker += 1
        if self.cooldown_tracker > 300:
            self.conscious = True
            self.cooldown_tracker = 0
            self.update_action(4)
            self.update_animation()
        if self.conscious:
            self.move_counter += 1
            if self.move_counter > 2 * data.settings.SCALA:
                self.direction *= -1
                self.move_counter = 0
        self.update(display, tile_rects, left, right, jump, shoot)


    def update(self, display, tile_rects, left, right, jump, shoot):
        '''
        Update is used for player controlled characters without the help of ai()-method.
        First we check if the character is controlled by the player
        '''
        self.current_time = pygame.time.get_ticks()
        if self.control:
            if left:
                self.direction = -1
            if right:
                self.direction = 1
            if shoot:
                pass
            self.moving_left = left
            self.moving_right = right

            # Update animation depending on the action performed
            if left or right:  # Walking
                self.update_action(4)
            if jump:
                self.update_action(3)
                if self.air_timer < 6:
                    self.player_y_momentum = data.settings.GRAVITY
            else:  # Idling
                self.update_action(2)

        self.update_player_position(display, tile_rects)

    def update_conscious_position(self, tile_rects):
        self.player_movement = [0, 0]
        # The character is controlled by the player.
        if self.control:
            if self.moving_right:
                self.player_movement[0] += self.speed
            if self.moving_left:
                self.player_movement[0] -= self.speed

        # If the character is not controlled by the player,
        # they will walk in the starting location and a little slower.
        else:
            if self.direction == 1:
                self.player_movement[0] += self.speed - 1
            if self.direction == -1:
                self.player_movement[0] -= self.speed - 1

        self.player_movement[1] += self.player_y_momentum
        self.player_y_momentum += 0.3
        if self.player_y_momentum > 3:
            self.player_y_momentum = 3

        collisions = self.move(self.player_movement, tile_rects)

        if collisions['right'] or collisions['left'] and not self.control:
            self.direction *= -1
        if collisions['bottom']:
            self.player_y_momentum = 0
            self.air_timer = 0
        if collisions['top']:
            self.player_y_momentum += 1
        else:
            self.air_timer += 1

        self.update_animation()
        if self.player_movement[0] > 0:
            self.flip = False
        if self.player_movement[0] < 0:
            self.flip = True

    def update_player_position(self, display, tile_rects): #pylint: disable=too-many-branches
        '''
        Updates the character position on the screen.
        '''
        # Only conscious characters can move.
        if self.conscious:
            self.update_conscious_position(tile_rects)
        
            # Drawing methods for the player and thrown rocks
        self.image = pygame.transform.flip(self.image, self.flip, False)
        self.image.set_colorkey((255, 255, 255))
        display.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, movement, tiles):
        '''
        Testing if the player can move to the desired location.
        First checking which tiles the player hits if moved in the x-plane,
        memorizing the tiles that were hit, and checking based on movement
        whether those were in the way. After that, the same for the
        y-plane.
        '''
        self.collision_types = {'top': False,
                                'bottom': False, 'right': False, 'left': False}
        self.rect.x += movement[0]
        hit_list = self.collision_test(self.rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                self.rect.right = tile.left
                self.collision_types['right'] = True
            elif movement[0] < 0:
                self.rect.left = tile.right
                self.collision_types['left'] = True
        self.rect.y += movement[1]
        hit_list = self.collision_test(self.rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                self.rect.bottom = tile.top
                self.collision_types['bottom'] = True
            elif movement[1] < 0:
                self.rect.top = tile.bottom
                self.collision_types['top'] = True
        return self.collision_types

    def collision_test(self, rect, tiles):
        '''
        Returns all the tiles that player is hitting.
        '''
        self.hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                self.hit_list.append(tile)
        return self.hit_list

    def update_animation(self):
        '''
        Loops through the animations depending what the character is doing.
        '''
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > data.settings.ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        '''
        Updates the action the character is doing at any given moment.
        '''
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
