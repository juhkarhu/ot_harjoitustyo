#### Käyttöohje
Lataa projektin viimeisimmän releasen lähdekoodi etusivun sivupalkissa näkyvästä linkistä. 

### Ohjelman käynnistäminen
_Seuraavat komennot tulee suorittaa projektin src-kansiosssa._

Ennen ohjelman käynnistystä tulee asentaa tarvittavat riippuvuudet seuraavalla komennolla:
```bash
poetry install
```
Tämän jälkeen voit käynnistää pelin kirjoittamalla seuraavan komennon:
```bash
poetry run invoke start
```

### Ohjelman toiminta
Peli käynnistyy etusivulle:
![Etusivu](./images/aloitusruutu_real.JPG)

Etusivulla voit kirjoittaa käyttäjänimen pelin pistetaulukkoa varten (voit myös pyyhkiä virhelyönnit nimestäsi). Etusivu opastaa pelissä käytetyt näppäin- ja hiirikomennot. 

Kun painat Enteriä, niin peli alkaa ja näkymä muuttuu jotakuinkin seuraavanlaiseksi:
![Peliruutu](./images/peliruutu.JPG)
