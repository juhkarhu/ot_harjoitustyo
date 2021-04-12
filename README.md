# Lemmings-inspired game, Lemmingki

### Sovelluksen tarkoitus
Peli on yksinkertainen tasohyppely, johon on otettu vaikutteita Lemmingsistä. Pelihahmot ilmestyvät kentälle aloituskohdasta ja kävelevät ympäriinsä kunnes pelaaja valitsee sen. Valinnan jälkeen pelaajan tehtävä on ohjata hahmo kentän loppuun.
Pisteitä saa nopeudesta, kaikkien hahmojen tuomisesta kentän loppuun ja vihollisten tuhoamisesta. 

### Dokumentaatio
- [Tuntikirjanpito](./Documents/tuntukirjanpito.md)
- [Vaatimusmäärittely](./Documents/vaatimusmaarittely.md)

### Komentorivitoiminnot
#### Ohjelman suorittaminen
Ohjelma ainut vaatimus pygame-kirjasto.
*Komennot tulee ajaa src-kansiossa ollessa.*

Asenna riippuvuudet:
```bash
poetry install

Ohjelman voi suorittaa komennolla:
```bash
poetry run invoke start
```
#### Testaus
Testit suoritetaan komennolla:
```bash
poetry run invoke test
#### Testikattavuus
Testikattavuuden voi tarkistaa komennolla:
```bash
poetry run invoke coverage-report
```


#### Testaus
Testaus on vielä keskeneräinen, joten se ei ole vielä toiminnassa. 
