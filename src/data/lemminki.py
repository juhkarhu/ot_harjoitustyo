import pygame, os
import data.SETTINGS
import data.world


class Lemminki(pygame.sprite.Sprite):
    def __init__(self, character_type, scale, starting_pos, id):
        super().__init__()

        self.id = id
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

        self.load_images(character_type, scale, starting_pos)
        
  
    def load_images(self, character_type, scale, starting_pos):
        # All the animations have the same image as placeholder. Easy enough to edit if time allows. 
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        animation_types = ['attack', 'death', 'idle', 'jump', 'run']
        for animation in animation_types:
            temp_list = []
            path = f'{os.getcwd()}/img/{character_type}/{animation}'
            num_of_frames = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{character_type}/{animation}/{i}.png').convert_alpha()
                
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                # img.set_colorkey((255,255,255))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (starting_pos)

    def get_id(self):
        return self.id

    def take_control(self):
        self.control = True

    def give_control(self):
        self.control = False 

    # def throw_rock(self):
    #     if self.throw_cooldown == 0:
    #         self.throw_cooldown = 30
    #         rock = data.world.Rock(self.rect.centerx + (self.direction * self.rect.width), self.rect.centery, self.direction)
    #         self.thrown_rocks.add(rock)
       
    def ai(self, display, tile_rects, left, right, jump, shoot):
        self.move_counter += 1
        self.update(display, tile_rects, left, right, jump, shoot)
        if self.move_counter > 2 * data.SETTINGS.SCALA:
            self.direction *= -1
            self.move_counter = 0

    def update(self, display, tile_rects, left, right, jump, shoot):
        if self.control:
            if left:
                self.direction = -1
            if right:
                self.direction = 1
            if shoot:
                pass
                # self.throw_rock()
            self.moving_left = left
            self.moving_right = right

            # Update animation depending on the action performed
            if left or right: # Walking
                self.update_action(4)
            if jump:
                self.update_action(3)
                if self.air_timer < 6:
                    self.player_y_momentum = data.SETTINGS.GRAVITY
            else: # Idling
                self.update_action(2)

        self.update_player_position(display, tile_rects)

    def update_player_position(self, display, tile_rects):
        # Movement is an array, where [0] is x-movement and [1] is y-movement.
        self.player_movement = [0, 0]
        # The character is controlled by the player.
        if self.control:
            if self.moving_right:
                self.player_movement[0] += self.speed
            if self.moving_left:
                self.player_movement[0] -= self.speed
        
        # If the character is not controlled by the player, 
        # they will walk in the starting location and a little slower.
        if not self.control:
            if self.direction == 1:
                self.player_movement[0] += self.speed - 1
            if self.direction == -1:
                self.player_movement[0] -= self.speed - 1 
        
        # 
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

        # Drawing methods for the player and thrown rocks
        # self.thrown_rocks.update()
        # self.thrown_rocks.draw(display)
        self.image = pygame.transform.flip(self.image, self.flip, False)
        self.image.set_colorkey((255,255,255))
        display.blit(self.image, (self.rect.x, self.rect.y))


    '''Testing if the player can move to the desired location. First checking which tiles the player hits if moved in the x-plane,
    memorizing the tiles that were hit, and checking based on movement whether those were in the way. After that, the same for the 
    y-plane.'''
    def move(self, movement, tiles):
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
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

    ''' Returns all the tiles that player is hitting.'''
    def collision_test(self, rect, tiles):
        self.hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                self.hit_list.append(tile)
        return self.hit_list


    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > data.SETTINGS.ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        # self.mask = pygame.mask.from_surface(self.image)


    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()