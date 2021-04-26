import unittest
import pygame
from data.assets import lemminki
from data.assets.world import *
import data.settings


class TestPlayerClass(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.grass_image = pygame.image.load('img/ground_tiles/top_ground.png')
        self.dirt_image = pygame.image.load(
            'img/ground_tiles/middle_ground.png')
        self.test_map = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 10, 1],
            [1, 2, 2, 2, 2, 1, 1]
        ]

        self.tile_rects = []
        for y, row in enumerate(self.test_map):
            for x, tile in enumerate(row):
                if tile == 10:
                    self.new_player = lemminki.Lemminki(
                        'player', 2, (x * data.settings.TILE_SIZE, y * data.settings.TILE_SIZE), 1)
                    self.starting_position = (
                        x * data.settings.TILE_SIZE, y * data.settings.TILE_SIZE)
                if tile in [1, 2]:
                    self.tile_rects.append(pygame.Rect(
                        x * data.settings.TILE_SIZE, y * data.settings.TILE_SIZE, data.settings.TILE_SIZE, data.settings.TILE_SIZE))

    def test_animation_list(self):
        # Player has 5 different animation states
        self.assertEqual(len(self.new_player.animation_list), 5)
        # Each state has one (1) frame at the moment.
        self.assertEqual(len(self.new_player.animation_list[0]), 1)

    def test_get_player_id(self):
        self.assertEqual(self.new_player.get_id(), 1)

    def test_take_and_give_control(self):
        self.new_player.take_control()
        self.assertTrue(self.new_player.control)
        self.new_player.give_control()
        self.assertFalse(self.new_player.control)

    def test_player_hits_wall_on_right(self):
        # TODO Finish it.
        self.left = True
        self.right = False
        self.jump = False
        self.new_player.moving_right = True

        # Created player is controlled automatically.
        self.assertFalse(self.new_player.control)

        # for i in range(51):
        #     self.new_player.update(self.screen, self.tile_rects, self.left, self.right, self.jump)
        #     self.assertTrue(self.new_player.moving_right)
