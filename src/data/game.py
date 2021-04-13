import pygame, sys, os
import pygame.locals
from pygame.constants import MOUSEBUTTONDOWN
import data.lemminki
import data.SETTINGS
import data.world


class Game:
    def __init__(self):
        pygame.init()
        self.set_up_player_variables()
        self.load_game_data()
        self.read_map_data()
        
        self.game_loop()

    def set_up_player_variables(self):
        self.character_scale = 3
        self.throw_cooldown = 0
        self.control = False
        self.left = False
        self.right = False
        self.jump = False
        self.shoot = False
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
        self.door_list = pygame.sprite.Group()
        self.thrown_rocks = pygame.sprite.Group()
        self.num_of_players_spawned = 0

        self.load_tile_images()      

        self.game_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
            [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 2, 3, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 1, 2, 2, 2, 2, 0, 0, 0, 1],
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

        self.height = len(self.game_map)
        self.width = len(self.game_map[0])
        data.SETTINGS.SCREEN_HEIGHT = data.SETTINGS.SCALA * self.height
        data.SETTINGS.SCREEN_WIDTH = data.SETTINGS.SCALA * self.width
        self.WINDOW_SIZE = (data.SETTINGS.SCREEN_HEIGHT, data.SETTINGS.SCREEN_WIDTH)
        self.screen = pygame.display.set_mode((data.SETTINGS.SCREEN_WIDTH, data.SETTINGS.SCREEN_HEIGHT))
        pygame.display.set_caption('Lemminki')
        # self.display = pygame.Surface((300, self.screen_width))
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if self.control:
                    if event.key == pygame.K_a:
                        self.left = True
                    if event.key == pygame.K_d:
                        self.right = True
                    if event.key == pygame.K_SPACE:
                        if self.throw_cooldown == 0:
                            self.throw_cooldown = 25
                            rock = data.world.Rock(self.player.rect.centerx + (self.player.direction * self.player.rect.width), self.player.rect.centery, self.player.direction)
                            self.thrown_rocks.add(rock)
                        self.shoot = True
                    if event.key == pygame.K_w and not self.jump:
                        self.jump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.left = False
                if event.key == pygame.K_d:
                    self.right = False
                if event.key == pygame.K_SPACE:
                    self.shoot = False
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
                    new_player = data.lemminki.Lemminki('player', self.character_scale, (self.starting_position), id)
                    self.player_sprites.add(new_player)
                    self.num_of_players_spawned += 1


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
            if self.throw_cooldown > 0:
                self.throw_cooldown -= 1
            self.clock.tick(60)
            self.draw_screen()
            self.check_events()
            pygame.display.flip()


    '''
    Reads the map array and assigns objects depending on the value on the array. 
    1 and 2 are ground tiles.
    3 is an enemy.
    10 is the starting locations for the player. 
    8 is the door that finishes the level.
    '''
    def read_map_data(self):
        self.tile_rects = []     
        for y, row in enumerate(self.game_map):
            for x, tile in enumerate(row):
                if tile == 10:
                    self.starting_pos = None
                    self.starting_position = (x * data.SETTINGS.TILE_SIZE, y * data.SETTINGS.TILE_SIZE)
                if tile in [1, 2]:
                    self.tile_rects.append(pygame.Rect(x * data.SETTINGS.TILE_SIZE, y * data.SETTINGS.TILE_SIZE, data.SETTINGS.TILE_SIZE, data.SETTINGS.TILE_SIZE))
                if tile == 1:
                    self.tile_rects.append(pygame.Rect(x * data.SETTINGS.TILE_SIZE, y * data.SETTINGS.TILE_SIZE, data.SETTINGS.TILE_SIZE, data.SETTINGS.TILE_SIZE))
                    tile = data.world.Tile(x * data.SETTINGS.TILE_SIZE, y * data.SETTINGS.TILE_SIZE, self.dirt_image)
                    self.map_sprites.add(tile)
                if tile == 2:
                    self.tile_rects.append(pygame.Rect(x * data.SETTINGS.TILE_SIZE, y * data.SETTINGS.TILE_SIZE, data.SETTINGS.TILE_SIZE, data.SETTINGS.TILE_SIZE))
                    tile = data.world.Tile(x * data.SETTINGS.TILE_SIZE, y * data.SETTINGS.TILE_SIZE, self.grass_image)
                    self.map_sprites.add(tile)
                if tile == 3:
                    id = os.urandom(16).hex()
                    new_npc = data.lemminki.Lemminki('enemy', self.character_scale, (x * data.SETTINGS.TILE_SIZE, y * data.SETTINGS.TILE_SIZE), id)
                    self.npc_list.add(new_npc)
                if tile == 8:
                    door = data.world.Door(x * data.SETTINGS.TILE_SIZE, y * data.SETTINGS.TILE_SIZE)
                    self.map_sprites.add(door)
                    self.door_list.add(door)



    def draw_screen(self):
        self.screen.fill((146,244,255))
        self.map_sprites.draw(self.screen)
        self.thrown_rocks.update()
        self.thrown_rocks.draw(self.screen)
        if self.control:
            for door in self.door_list:
                if self.player.rect.colliderect(door.rect):
                    #TODO Onko kaikki paasseet loppuun.
                    print('one point awarded')
        for rock in self.thrown_rocks:
            for npc in self.npc_list:
                if rock.rect.colliderect(npc.rect):
                    print('point for hitting enemy. Enemy goes to sleep for X amount of time before he wakes back up.')
        
        for player in self.player_sprites:
            player.update(self.screen, self.tile_rects, self.left, self.right, self.jump, self.shoot)
        for npc in self.npc_list:
            npc.ai(self.screen, self.tile_rects, self.left, self.right, self.jump, self.shoot)
