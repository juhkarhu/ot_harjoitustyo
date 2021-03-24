import unittest
from maksukortti import Maksukortti
from kassapaate import Kassapaate

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_uuden_kassapaatteen_rahamaara_on_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 1000)
        
    def test_uudessa_kassapaatteessa_ei_myytyja_lounaita(self):
        self.assertEqual(self.kassapaate.maukkaat, 0) and self.assertEqual(self.kassapaate.edulliset, 0)

    '''
    Kateisostot edulliseen
    '''
    def test_edullinen_osto_kateisella_riittavalla_maksulla_toimii(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(250), 10)

    def test_onnistunut_edullinen_osto_kateisella_kasvattaa_myyntia(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_edullinen_lounas_ei_onnistu_ja_rahat_palautetaan(self):
        self.kassapaate.syo_edullisesti_kateisella(230)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 1000) and self.assertEqual(self.kassapaate.edulliset, 0)
    '''
    Kateisostot maukkaaseen
    '''
    def test_maukas_osto_kateisella_riittavalla_maksulla_toimii(self):
            self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(410), 10)

    def test_onnistunut_maukas_osto_kateisella_kasvattaa_myyntia(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.maukkaat, 1)
    
    def test_maukas_lounas_ei_onnistu_ja_rahat_palautetaan(self):
        self.kassapaate.syo_maukkaasti_kateisella(230)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 1000) and self.assertEqual(self.kassapaate.maukkaat, 0)
    '''
    Edullisten korttiostojen testit
    '''
    def test_korttiosto_toimii_edulliseen_ja_myydyt_lounaat_lisaantyy(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_korttiosto_raha_ei_riita_edulliseen_lounasmaara_ei_muutu_ja_palautetaan_false(self):
        maksukortti = Maksukortti(230)
        self.assertFalse(self.kassapaate.syo_edullisesti_kortilla(maksukortti))

    def test_kassan_raha_ei_muutu_korttiostoissa_edullinen_lounas(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 1000)
    '''
    Maukkaiden korttiostojen testit
    '''
    def test_korttiosto_toimii_maukkaaseen_ja_myydyt_lounaat_lisaantyy(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_korttiosto_raha_ei_riita_maukkaaseen_lounasmaara_ei_muutu_ja_palautetaan_false(self):
        maksukortti = Maksukortti(230)
        self.assertFalse(self.kassapaate.syo_maukkaasti_kortilla(maksukortti))

    def test_kassan_raha_ei_muutu_korttiostoissa_maukas_lounas(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 1000)
    
    
    def test_kortille_rahaa_ladattaessa_kassaraha_ja_kortin_saldo_nousee(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 2000) and self.assertEqual(self.maksukortti.saldo, 2000)

    def test_kortille_ladataan_negatiivinen_maara_rahaa_palautetaan_false(self):
        self.assertFalse(self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -1000))