import unittest
import data.points


class TestPointsClass(unittest.TestCase):

    def test_writing_to_scorelist_works(self):
        scorelist_beginning = data.points.read_points()
        data.points.write_points('testi', 10)
        scorelist_final = data.points.read_points()
        self.assertEqual(len(scorelist_beginning)+1, len(scorelist_final))

    