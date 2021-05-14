# Lemmingki

### Sovelluksen tarkoitus
Peli on yksinkertainen tasohyppely, johon on otettu vaikutteita Lemmingsistä. Pelihahmot ilmestyvät kentälle aloituskohdasta ja kävelevät ympäriinsä kunnes pelaaja valitsee sen. Valinnan jälkeen pelaajan tehtävä on ohjata hahmo kentän loppuun.
Pisteitä saa nopeudesta, kaikkien hahmojen tuomisesta kentän loppuun ja vihollisten tuhoamisesta. 

### Dokumentaatio
- [Tuntikirjanpito](./Documents/tuntikirjanpito.md)
- [Vaatimusmäärittely](./Documents/vaatimusmaarittely.md)
- [Arkkitehtuuri](./Documents/arkkitehtuuri.md)
- [Käyttöohje](./Documents/kayttoohje.md)

### Release
- [Release Viikko 5](https://github.com/juhkarhu/ot_harjoitustyo/releases/tag/viikko5)
- [Release Viikko 6](https://github.com/juhkarhu/ot_harjoitustyo/releases/tag/viikko6)
- [Release Viikko 7](https://github.com/juhkarhu/ot_harjoitustyo/releases/tag/viikko7)

### Komentorivitoiminnot
#### Ohjelman suorittaminen
Ohjelma ainut vaatimus on pygame-kirjasto.  
*Komennot tulee ajaa src-kansiossa ollessa.*

Asenna riippuvuudet:
```
poetry install
```

Ohjelman voi suorittaa komennolla:
```
poetry run invoke start
```
#### Testaus
Testit suoritetaan komennolla:
```
poetry run invoke test
```

#### Testikattavuus
Testikattavuuden voi tarkistaa komennolla:
```
poetry run invoke coverage-report
```

#### Pylint
Tiedoston [.pylintrc](./src/.pylintrc) määrittelemät tarkistukset suoritetaan komennolla:
```
poetry run invoke lint
```
