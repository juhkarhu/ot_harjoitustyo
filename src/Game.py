import pygame
import os
from Player import Player
from Enemy import Enemy
from pygame.constants import MOUSEBUTTONDOWN
from SETTINGS import *
from World import *



class Game:
    def __init__(self):
        pygame.init()
        # self.tile_list = pygame.sprite.Group()
        self.tile_list = []
        
        self.load_tile_images()
        self.new_game()
        
        
        self.load_tiles()
        
        self.game_loop()


    def load_tile_images(self):
        # TODO Change tile textures
        self.grass_img = pygame.image.load('./img/ground_tiles/top_ground.png')
        self.dirt_img = pygame.image.load('./img/ground_tiles/middle_ground.png')
        self.exit_img = pygame.image.load('./img/robo.png')



    def new_game(self):

        self.interval = 1000 # Can be used to raise difficulty level
        self.ADD_LEMMING = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADD_LEMMING, self.interval)


        # Sprite Groups
        self.player_sprites = pygame.sprite.Group()
        self.num_of_players_spawned = 0
        self.enemy_sprites = pygame.sprite.Group()
        self.door_list = pygame.sprite.Group()
        self.controlled_player_list = pygame.sprite.Group()

        self.map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 1],
            [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 2, 3, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 2, 2, 0, 0, 0, 2, 2, 1, 2, 2, 2, 2, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
            [1, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]

        self.height = len(self.map)
        self.width = len(self.map[0])
        self.screen_height = SCALA * self.height
        self.screen_width = SCALA * self.width
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height+100))
        pygame.display.set_caption("Lemmingki")

        self.clock = pygame.time.Clock()
        self.score = 0

        # Variable to count how many players have passed. 
        self.players_passed = 0

        # Num. of players on screen. 
        self.max_players = 3

        # Player controls
        self.player = None
        self.left = False
        self.right = False
        self.jump = False
        self.control = False
        
        
        self.start_pos = (100, 800)
        
    def check_ending_conditions(self):
        if pygame.sprite.groupcollide(self.player_sprites, self.door_list, False, False):
            if self.control:
                for entity in self.controlled_player_list:
                    entity.give_control()
                    entity.kill()
                self.players_passed += 1
                self.player = None
                self.control = False
                self.controlled_player_list.empty()
        if self.players_passed == self.max_players:
            print('All are safe!!')
        




    def load_tiles(self):      
        row_count = 0
        for row in self.map:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(self.dirt_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(self.grass_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    # tile = Tile(x, y, img, img_rect)
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    enemy = Enemy('enemy', col_count*SCALA, row_count*SCALA, 1.3, 5, 1)
                    self.enemy_sprites.add(enemy)
                if tile == 8:
                    door = Door(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    self.door_list.add(door)
                col_count += 1
            row_count += 1

    def game_loop(self):
        while True:
            self.clock.tick(30)
            self.check_events()
            self.draw_screen()
            self.check_ending_conditions()

    '''Go over the events (controls, mouse clicks and spawning of lemmings).'''
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_a:
                    self.left = True
                if event.key == pygame.K_d:
                    self.right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.left = False
                if event.key == pygame.K_d:
                    self.right = False

            if event.type == MOUSEBUTTONDOWN:
                self.x, self.y = event.pos
                for entity in self.player_sprites:
                    if entity.rect.collidepoint(self.x, self.y):
                        self.check_control_conditions(entity)
            if event.type == self.ADD_LEMMING:
                if self.num_of_players_spawned < self.max_players:
                    # Needs attributes: character_type, x, y, scale, speed, id (randomly generated)
                    id = os.urandom(16).hex()
                    new_lemming = Player('player', self.start_pos[0], self.start_pos[1], 1.3, 5, id)
                    self.player_sprites.add(new_lemming)
                    self.num_of_players_spawned += 1



    '''Check whether the clicked character may be controlled or not.
    The Player can have only one controllable character at a time.'''
    def check_control_conditions(self, entity):
        if len(self.controlled_player_list) < 1:
            #TODO Only one controllable character at a time
            if not self.control:
                self.player = entity
                self.controlled_player_list.add(entity)
                self.control = True
                entity.take_control()
            elif self.control:
                self.player = None
                self.controlled_player_list.empty()
                self.control = False
                entity.give_control()
        else:
            self.player = None
            self.controlled_player_list.empty()
            self.control = False
            entity.give_control()

    def draw_screen(self):
        self.screen.fill(BACKGROUND_COLOUR)

        # The info for the score goes on this bar.
        pygame.draw.rect(self.screen, BLACK, (0, self.screen_height, self.screen_width, 100))

        # Draw tiles on screen. Every tile consists of image and the image rectangle
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])
        # self.tile_list.draw(self.screen)
        self.door_list.draw(self.screen)

        # Draw enemies on screen
        for entity in self.enemy_sprites:
            entity.ai(self.tile_list)
            entity.draw(self.screen)

        # Draw player characters
        for player in self.player_sprites:
            player.update(self.tile_list, self.left, self.right)
            player.draw(self.screen)

        pygame.display.flip()