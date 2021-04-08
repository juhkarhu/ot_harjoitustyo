import pygame
import os
from Player import Player
from Enemy import Enemy
from pygame.constants import MOUSEBUTTONDOWN
from SETTINGS import *
from Door import Door


class Game:
    def __init__(self):
        pygame.init()
        SCALA = 50
        self.tile_size = 50
        self.tile_list = []
        self.interval = 1000 # Can be used to raise difficulty level
        self.load_tile_images()
        self.new_game()
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.screen_height = SCALA * self.height
        self.screen_width = SCALA * self.width
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height+100))
        self.clock = pygame.time.Clock()
        self.load_tiles()
        self.score = 0
        # If the player touches the door, game ends succesfully
        self.game_pass = 0
     
        self.max_lemmings = 3

        # Player controls
        self.player = None
        self.left = False
        self.right = False
        self.jump = False
        self.control = False
        self.controlled_player_list = []
        
        self.start_pos = (100, 800)
        pygame.display.set_caption("Lemmingki")
        self.game_loop()


    def load_tile_images(self):
        # TODO Change tiles?
        self.grass_img = pygame.image.load('./img/ground_tiles/top_ground.png')
        self.dirt_img = pygame.image.load('./img/ground_tiles/middle_ground.png')
        self.exit_img = pygame.image.load('./img/robo.png')



    def new_game(self):
        self.ADD_LEMMING = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADD_LEMMING, self.interval)
        self.player_sprites = pygame.sprite.Group()
        self.all_lemmings = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.door_list = pygame.sprite.Group()

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

    def load_tiles(self):
        row_count = 0
        for row in self.map:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(self.dirt_img, (self.tile_size, self.tile_size))
                    # tile = Tile(img, col_count, row_count, self.tile_size, 'middle_ground')
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    # mask = pygame.mask.from_surface(img)
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(
                        self.grass_img, (self.tile_size, self.tile_size))
                    # tile = Tile(img, col_count, row_count, self.tile_size, 'top_g')
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    # mask = pygame.mask.from_surface(img)
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    enemy = Enemy('enemy', col_count*SCALA, row_count*SCALA, 1.3, 5, 1)
                    self.enemy_sprites.add(enemy)
                if tile == 8:
                    door = Door(col_count * self.tile_size, row_count * self.tile_size, self.tile_size)
                    self.door_list.add(door)
                col_count += 1
            row_count += 1

    def game_loop(self):
        while True:
            self.clock.tick(30)
            self.check_events()
            self.draw_screen()

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
                for entity in self.all_lemmings:
                    if entity.rect.collidepoint(self.x, self.y):
                        #TODO Only one controllable character at a time
                        if not self.control and len(self.controlled_player_list) < 1:
                            self.player = entity
                            self.controlled_player_list.append(entity.get_id())
                            self.control = True
                            entity.take_control()
                        else:
                            self.player = None
                            self.control = False
                            entity.take_control()
            if event.type == self.ADD_LEMMING:
                if len(self.player_sprites) < self.max_lemmings:
                    # Needs attributes: character_type, x, y, scale, speed, id (randomly generated)
                    id = os.urandom(16).hex()
                    new_lemming = Player('player', self.start_pos[0], self.start_pos[1], 1.3, 5, id)
                    self.all_lemmings.add(new_lemming)
                    self.player_sprites.add(new_lemming)


    def draw_screen(self):
        self.screen.fill(BACKGROUND_COLOUR)

        pygame.draw.rect(self.screen, BLACK, (0, self.screen_height, self.screen_width, 100))

        # Draw tiles on screen. Every tile consists of image and the image rectangle
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])
            
        self.door_list.draw(self.screen)

        # Draw enemies on screen
        # self.enemy_sprites.draw(self.screen)
        for entity in self.enemy_sprites:
            entity.ai(self.tile_list)
            entity.draw(self.screen)

        if pygame.sprite.groupcollide(self.all_lemmings, self.door_list, False, False):
            self.game_over = -1
            print('peli ohi')

        # Draw player characters
        for entity in self.all_lemmings:
            entity.update(self.tile_list, self.left, self.right)
            entity.draw(self.screen)

        pygame.display.flip()