import pygame, sys, os
from pygame.locals import *
from pygame.constants import MOUSEBUTTONDOWN
from player import Player
from enemy import Enemy
from SETTINGS import *
from world import *


class Game:
    def __init__(self):
        pygame.init()
        self.load_game_data()
        self.read_map_data()
        self.set_up_player_variables()
        self.game_loop()

    def set_up_player_variables(self):

        self.control = False
        self.left = False
        self.right = False
        self.jump = False
        self.interval = 1600
        self.ADD_LEMMING = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADD_LEMMING, self.interval)

        self.player = None
        self.player_id = 0


    def load_tile_images(self):
        self.grass_image = pygame.image.load('img/ground_tiles/top_ground.png')
        self.dirt_image = pygame.image.load('img/ground_tiles/middle_ground.png')


    def load_game_data(self):
        self.controlled_player_list = pygame.sprite.Group()
        self.npc_list = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.map_sprites = pygame.sprite.Group()
        self.num_of_players_spawned = 0

        self.load_tile_images()      

        self.TILE_SIZE = self.grass_image.get_width()
        self.game_map = [
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
            [1, 0, 0, 10, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ] 

        self.clock = pygame.time.Clock()
        self.max_players = 2
        self.controlled = False

        self.height = len(self.game_map)
        self.width = len(self.game_map[0])
        self.screen_height = SCALA * self.height
        self.screen_width = SCALA * self.width
        self.WINDOW_SIZE = (self.screen_height, self.screen_width)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Lemmingki')
        # self.display = pygame.Surface((300, self.screen_width))
    
    def check_events(self):
        self.events = []
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_a:
                    self.left = True
                if event.key == pygame.K_d:
                    self.right = True
                if event.key == pygame.K_w and not self.jump:
                    self.jump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.left = False
                if event.key == pygame.K_d:
                    self.right = False
                if event.key == pygame.K_w:
                    self.jump = False

            if event.type == MOUSEBUTTONDOWN:
                self.x, self.y = event.pos
                for unit in self.player_sprites:
                    if unit.rect.collidepoint(self.x, self.y):
                        self.check_control_conditions(unit)
            if event.type == self.ADD_LEMMING:
                if self.num_of_players_spawned < self.max_players:
                    id = os.urandom(16).hex()
                    new_player = Player('player', 4, (self.starting_position), id)
                    self.player_sprites.add(new_player)
                    self.num_of_players_spawned += 1
            else:
                self.events.append(event)


    '''Check whether the clicked character may be controlled or not.
    The Player can have only one controllable character at a time.'''
    def check_control_conditions(self, entity):
        pass
        # if entity.get_id() != self.player_id:
        #     self.player_id = entity.get_id()
        #     self.player = entity
        #     self.controlled_player_list.add(entity)
        #     self.control = True
        #     entity.take_control()
        # else:  
            



        # print(entity.get_id(), 'ja', self.player.get_id())
        if len(self.controlled_player_list) < 1:
            print(entity.get_id())
            print('ja', self.player_id)
            #TODO Only one controllable character at a time. Does not work as of yet.
            if not self.control:
                self.player_id = entity.get_id()
                self.player = entity
                self.controlled_player_list.add(entity)
                self.control = True
                entity.take_control()
            elif self.control:
                print('EIEIEIE')
                print(entity.get_id(), 'ja', self.player.get_id())
                self.player = None
                self.controlled_player_list.empty()
                self.control = False
                entity.give_control()
        else:
            self.player_id = None
            self.player = None
            self.controlled_player_list.empty()
            self.control = False
            entity.give_control()
        

    def game_loop(self):
        while True:
            self.clock.tick(60)
            self.draw_screen()
            self.check_events()
            pygame.display.flip()



    def read_map_data(self):
        self.tile_rects = []     
        for y, row in enumerate(self.game_map):
            for x, tile in enumerate(row):
                if tile == 10:
                    self.starting_pos = None
                    print('starting_pos here!')
                    self.starting_position = (x * TILE_SIZE, y * TILE_SIZE)
                    print(self.starting_position)
                if tile in [1, 2]:
                    self.tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                if tile == 1:
                    self.tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    tile = Tile(x * TILE_SIZE, y * TILE_SIZE, self.dirt_image)
                    self.map_sprites.add(tile)
                if tile == 2:
                    self.tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    tile = Tile(x * TILE_SIZE, y * TILE_SIZE, self.grass_image)
                    self.map_sprites.add(tile)
                if tile == 3:
                    id = os.urandom(16).hex()
                    new_npc = Enemy('enemy', 4, (x * TILE_SIZE, y * TILE_SIZE), id)
                    self.npc_list.add(new_npc)
                x += 1
            y += 1

    def draw_screen(self):
        self.screen.fill((146,244,255))
        self.map_sprites.draw(self.screen)
        for player in self.player_sprites:
            player.update(self.screen, self.tile_rects, self.left, self.right, self.jump)
        for npc in self.npc_list:
            npc.ai(self.screen, self.tile_rects, self.left, self.right, self.jump)

peli = Game()
