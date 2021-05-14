import unittest
import pygame

from data.assets.map import Map



class TestMapClass(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.map = Map()
        self.map.read_map_data()

    def test_return_npc_list(self):
        npc_list = self.map.get_npc_list()
        self.assertEqual(len(npc_list), 3)

    def test_return_door_list(self):
        self.assertEqual(len(self.map.get_door_list()),1)

    def test_return_map_sprites(self):
        self.assertEqual(len(self.map.get_map_sprites()),132)

    def test_return_game_map_height(self):
        self.assertEqual(self.map.get_game_map_height(),19)

    def test_return_game_map_width(self):
        self.assertEqual(self.map.get_game_map_width(),20)

    def test_return_game_map(self):
        map = self.map.get_game_map()
        self.assertEqual(len(map), 19)