import unittest
import pygame
from Game import *
from Player import *

class TestPlayerClass(unittest.TestCase):
    def setUp(self):
        # peli = Game()
        new_lemming = Player('player', 1, 1, 1.3, 5, id)

    def test_all_animations_load(self):
        self.assertEqual(self.new_lemming.get_animation_list(), 3)