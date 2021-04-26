import unittest
import pygame
import data.world


class TestWorldClass(unittest.TestCase):
    def setUp(self):
        self.door = data.world.Door(10,20)
        self.grass_tile = data.world.Tile(10, 70, pygame.image.load('img/ground_tiles/top_ground.png'))
        self.rock = data.world.Rock(10,0,1)

    def test_door_is_where_it_spawned(self):
        self.assertEqual(self.door.rect.x, 10)
        self.assertEqual(self.door.rect.y, 20)

    def test_tile_is_in_spawn_location(self):
        self.assertEqual(self.grass_tile.rect.x, 10)
        self.assertEqual(self.grass_tile.rect.y, 70)
        
    def test_rock_goes_right_on_spawn(self):
        self.assertEqual(self.rock.direction, 1)

    def test_rock_moves_on_update(self):
        # Rock is a 20 pixel wide square. It's rect is positioned self.rect.center = (x,y),
        # so it's center on spawn, and so it's rect.x is -10. When it has flown for 1 frame,
        # it's leftmost side is at position X = 10.
        self.rock.update()
        self.assertEqual(self.rock.rect.x, 10)
        self.rock.update()
        self.assertEqual(self.rock.rect.x, 20)
 
