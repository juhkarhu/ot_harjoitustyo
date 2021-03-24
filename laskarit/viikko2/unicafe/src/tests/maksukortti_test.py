import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_on_oikein_alussa(self):
        self.assertEqual(str(self.maksukortti), 'saldo: 10.0')

    def test_rahan_lataaminen_kasvattaa_saldoa(self):
        self.maksukortti.lataa_rahaa(1000)
        self.assertEqual(str(self.maksukortti), 'saldo: 20.0')

    def test_rahan_ottamien_vahentaa_saldoa(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(str(self.maksukortti), 'saldo: 5.0')

    def test_rahaa_ei_voi_nostaa_enempaa_kuin_saldoa(self):
        self.maksukortti.ota_rahaa(200)
        self.assertEqual(str(self.maksukortti), 'saldo: 8.0')

    def test_rahan_ottaminen_palauttaa_true_jos_onnistuu(self):
        self.assertTrue(self.maksukortti.ota_rahaa(500))

    def test_rahan_ottaminen_palauttaa_false_jos_epaonnistuu(self):
        self.assertFalse(self.maksukortti.ota_rahaa(1500))