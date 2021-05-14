import unittest
import pygame
import os
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
            [1, 0, 10, 0, 3, 0, 1],
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
                        x * data.settings.TILE_SIZE, y * data.settings.TILE_SIZE, data.settings.TILE_SIZE, 
                        data.settings.TILE_SIZE))
                if tile == 3:
                    id_num = os.urandom(16).hex()
                    self.new_npc = lemminki.Lemminki('enemy', data.settings.CHARACTER_SCALE, (
                        x * data.settings.TILE_SIZE, y * data.settings.TILE_SIZE),
                        id_num)
                    


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

    def test_characters_are_controlled_automatically(self):
        # X positions can not be the same if player is not controlled, since the character is moving.
        self.assertFalse(self.new_player.control)
        self.assertFalse(self.new_npc.control)
        self.assertEqual(self.new_npc.direction, 1)

    def test_ai_movement_works(self):
        previous_x_position = self.new_npc.rect.x
        self.new_npc.ai_movement(self.screen, self.tile_rects, False, False, False, False)
        self.assertNotEqual(previous_x_position, self.new_npc.rect.x)

    def test_enemy_gets_hit(self):
        self.assertTrue(self.new_npc.conscious)
        self.new_npc.get_hit_enemy()
        self.new_npc.ai_movement(self.screen, self.tile_rects, False, False, False, False)
        self.assertFalse(self.new_npc.conscious)

    def test_player_can_move_right(self):
        # Player can be taken control of
        self.new_player.take_control()
        self.assertTrue(self.new_player.control)
        # Player can move to the right
        self.new_player.update(self.screen, self.tile_rects, False, True, False, False)
        self.assertEqual(self.new_player.direction, 1)

    def test_player_can_move_left(self):
        # Player can be taken control of
        self.new_player.take_control()
        self.assertTrue(self.new_player.control)
        # Player can move to the left
        # Player position has changed
        previous_x_position = self.new_player.rect.x
        self.new_player.update(self.screen, self.tile_rects, True, False, True, False)
        self.assertNotEqual(previous_x_position, self.new_player.rect.x)
        self.assertEqual(self.new_player.direction, -1)

    def test_player_can_move_right(self):
        # Player can be taken control of
        self.new_player.take_control()
        self.assertTrue(self.new_player.control)
        # Player can move to the right
        # Player position has changed
        previous_x_position = self.new_player.rect.x
        self.new_player.update(self.screen, self.tile_rects, False, True, False, False)
        self.assertNotEqual(previous_x_position, self.new_player.rect.x)
        self.assertEqual(self.new_player.direction, 1)
        
    def test_player_gets_hit(self):
        hitpoints_at_first = self.new_player.get_hitpoints()
        self.new_player.get_hit_player()
        hitpoints_after = self.new_player.get_hitpoints()
        self.assertEqual(hitpoints_at_first, hitpoints_after)

    def test_ai_unconscious_movement(self):
        move_counter_before = self.new_npc.move_counter
        self.new_npc.ai_movement(self.screen, self.tile_rects, False, True, False, False)
        move_counter_after = self.new_npc.move_counter
        self.assertEqual(move_counter_before, move_counter_after - 1)


        
