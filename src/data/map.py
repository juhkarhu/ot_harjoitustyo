import os
import pygame
import data.settings #pylint: disable=import-error
from data.assets import lemminki, world #pylint: disable=import-error

class Map:
    def __init__(self):

        self.load_dirt_image()
        self.load_grass_image()

        self.npc_list = pygame.sprite.Group()
        self.map_sprites = pygame.sprite.Group()
        self.door_list = pygame.sprite.Group()


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
            [1, 0, 10, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
            [1, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        #Pylint error handling
        self.tile_rects = None
        self.starting_position = None



    def get_npc_list(self):
        return self.npc_list

    def get_map_sprites(self):
        return self.map_sprites

    def get_door_list(self):
        return self.door_list

    def get_game_map(self):
        return self.game_map

    def get_starting_position(self):
        return self.starting_position

    def load_grass_image(self):
        self.grass_image = pygame.image.load('img/ground_tiles/top_ground.png')
        return self.grass_image

    def load_dirt_image(self):
        self.dirt_image = pygame.image.load('img/ground_tiles/middle_ground.png')
        return self.dirt_image

    def load_game_map(self):
        # Only one map, but it can be easily modified (or make external app for array manipulation)
        return self.game_map


    def read_map_data(self):
        '''
        Reads the map array and assigns objects depending on the value on the array.
        1 and 2 are ground tiles,
        3 is an enemy,
        10 is the starting locations for the player,
        8 is the door that finishes the level.
        '''

        self.tile_rects = []
        for row_num, row in enumerate(self.game_map):
            for col_num, tile in enumerate(row):
                if tile == 10:

                    self.starting_position = (
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE)
                if tile in [1, 2]:
                    self.tile_rects.append(pygame.Rect(
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE,
                        data.settings.TILE_SIZE, data.settings.TILE_SIZE))
                if tile == 1:
                    self.tile_rects.append(pygame.Rect(
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE,
                        data.settings.TILE_SIZE, data.settings.TILE_SIZE))
                    tile = world.Tile(
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE,
                        self.dirt_image)
                    self.map_sprites.add(tile)
                if tile == 2:
                    self.tile_rects.append(pygame.Rect(
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE,
                        data.settings.TILE_SIZE, data.settings.TILE_SIZE))
                    tile = world.Tile(
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE,
                        self.grass_image)
                    self.map_sprites.add(tile)
                if tile == 3:
                    id_num = os.urandom(16).hex()
                    new_npc = lemminki.Lemminki('enemy', data.settings.CHARACTER_SCALE, (
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE), id_num)
                    self.npc_list.add(new_npc)
                if tile == 8:
                    door = world.Door(
                        col_num * data.settings.TILE_SIZE, row_num * data.settings.TILE_SIZE)
                    self.map_sprites.add(door)
                    self.door_list.add(door)
        return self.tile_rects
