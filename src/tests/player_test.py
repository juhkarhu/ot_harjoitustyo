import unittest
from data.player import *

class TestPlayerClass(unittest.TestCase):
    def setUp(self):
        print('set up goes here') 
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.new_player = Player('player', 4, (100, 100), id)
        

    def test_animation_list(self):
        # Player has 5 different animation states
        self.assertEqual(len(self.new_player.animation_list), 5)
        # Each state has one (1) frame at the moment. 
        self.assertEqual(len(self.new_player.animation_list[0]), 1)
