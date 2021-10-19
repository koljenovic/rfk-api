# RFK RESTful API 0.3.4
**RFK RESTful API** omogućava jednostavan HTTP REST pristup lokalnim legacy DBF "*bazama podataka*" originalno korištenim u programskim jezicima Clipper i Visual FoxPro. Generički API podržava čitanje i izmjenu postojećih kao i dodavanje novih zapisa kroz emulaciju `SELECT`, `UPDATE` i `INSERT` SQL DML iskaza nad .DBF *tabelama* (datotekama) unutar `data` direktorija, brisanje nije podržano.
    
**Ne preporučuje se korištenje .DBF datoteka za trajno spremanje podataka u savremenim programskim rješenjima**, ovaj API prvenstveno služi za čitanje podataka zarobljenih u .DBF formatu, migraciju i privremena integracijska rješenja, ukoliko trebate savremeno, pouzdano i jednostavno rješenje za lokalnu pohranu i pristup razmotrite SQLite datotečnu bazu podataka sa punom SQL podrškom.

API je prilično brz i vraća rezultate u vremenskom rasponu od 50 ms za jedan filtrirani rezultat do 500 ms za kompletnu tabelu od nekoliko stotina unosa, ukoliko zahtjevi traju duže od jedne sekunde provjerite vaš klijent, npr. Swagger probni klijent uključen u API dokumentaciji na URL-u datom ispod je relativno vrlo spor za sve odgovore sa preko par desetaka objekata, pa to imajte na umu prilikom korištenja dokumentacije. Za realniju sliku performansi koristite Insomnia, Postman ili Milkman API klijente.

**UPOZORENJE: korištnje `rfkapi` može uzrokovati nepopravljiva oštećenja vaše baze podataka, poželjno je da u svakom trenutku osigurate pravovremenu rezervnu kopiju vaših podataka, te da istu arhivirate u slučaju da tek naknadno otkrijete prouzrokovana oštećenja. Vjerovatnoću oštećenja možete umanjiti tako što nećete istovremeno koristiti druge programe koji vrše izmjene vaših podataka, korištenjem replicirane kopije podataka ili korištenjem samo metoda za čitanje podataka, tj. izbjegavanjem pisanja novih i izmjene postojećih podataka.**

*Napomena:* API je namjenski pisan za RFK računovodstvenu aplikaciju izrađenu u Clipperu, te je na njoj i testiran, no trebao bi bez većih izmjena podržavati bilo koju vrstu Clipper ili VFP .DBF podatkovne datoteke.

## Okruženje
Python 3.9+, linux, bash, pip

## Korištenje
Prije nego što prvi put pokrenete `rfkapi` potrebno je da sve `.DBF`, kao i ostale indeksne, memo i slične datoteke kojima želite prisupati stavite u jedan direktorij po izboru (*npr. `~/.rfk/data`*), putanju ka tom direktoriju koji sadrži vašu bazu neophodno je upisati u `RFK_HOME` varijablu okruženja (*en. environment variable*), bez ove postavke lokalna instanca će pri izvršavanju javljati grešku.

Nakon što ste postavili varijable okruženja u korijenskom `rfkapi` direktoriju izvršite instalaciju potrebnih biblioteka i pokrenite skriptu za pripremu podataka:

```bash
pip3 install -r requirements.txt
./prep_data.py
```

Izvršavanje skripte za pripremu podataka može potrajati nekoliko minuta zavisno od broja "tabela" u vašoj "baza podataka", te njihove kompleksnosti. `prep_data.py` vrši inferencije tipova podataka i oblika u kojem su zapisani unutar DBF datoteka, za sva polja, i za sve tabele, ovo ubrzava i pojednostavljuje korištenje samog interfejsa jer korisnik npr. ne mora razmišljati da li je podatak string ili broj, te da li je potrebno dodati nule na početku broja, te koliko nula je potrebno dodati. Nakon pokretanja skripta će dodati po jednu `.json` datoteku za svaku `.dbf` tabelu u vaš zadani `RFK_HOME` direktorij. **Prilikom izmjene šeme vaše DBF tabele neophodno je svaki put pobrisati njenu generisanu .json datoteku i ponovo pokrenete `prep_data.py` skriptu.**.

**UPOZORENJE:** `rfkapi` nema implementirane mehanizme zaštite sigurnosti, to je isključiva dužnost vas kao korisnika, za podešavanje pristupnih tokena za pisanje i brisanje ručno izmjenite vrijednosti u `swagger_server/controllers/authorization_controller.py` datoteci. Zadane vrijednosti autorizacijskih ključeva su date ispod i neophodno ih je slati prilikom svakog API zahtjeva u zavisnosti da li se radi o READ ili WRITE akciji. `rfkapi` ne implementira `https` sigurni transport te svi mrežni uređaji preko kojih prolazi vaš promet mogu vidjeti sadržaj vaših paketa, ukoliko želite otvoriti API prema drugim korisnicima van vaše mreže, implementirajte `nginx` obrnuti proxy i podesite `https` transport, mada se isto strogo ne preporučuje.

```python
{
    'X-API-RKEY': 'ggbTbze1HH9V5WHdctgcA8PKvnE1htlxWyczGHOgQHYHEpO13X',
    'X-API-WKEY': '1L7g6eq0LXil2xzoEv7CnwvglwWEu9PNgA2vgulNhAZR5HD1MM'
}
```

Nakon ovih pripremnih koraka za pokretanje servera u lokalnom okruženju u `rfkapi` korijenskom direktoriju unesite komandu:

```bash
# za probno okruženje
python3 -m swagger_server

# ili za produkcijsko okruženje
# UPOZORENJE: 0.0.0.0 SLUŠA NA SVIM ADRESAMA
gunicorn -w 4 -b 0.0.0.0:8844 "swagger_server.__main__:app()"
```

za detalju dokumentaciju samog interfejsa sada u web pregledniku otvorite:

```
http://localhost:8844/ui/
```

## Docker instanca
Pojedinačne korake kompilacije i pokretanja slike kao i prilagodbe volume `-v` data direktorija i lokalnog porta na kojem će server slušati podesite prvenstveno u `run_docker` izvršnoj datoteci. Zadano server sluša na portu **8844** i podatke kupi iz `~/.rfk/data` direktorija. Za više detalja referirajte se na docker dokumentaciju: https://docs.docker.com/engine/reference/commandline/run/

Za pokretanje `rfkapi` docker instance dovoljno je pokrenuti već pripremljene skripte za kompilaciju i pokretanje u korijenskom direktoriju, no prije toga potrebno je izvršiti pripremu data direktorija prema uputstvima datim u poglavlju iznad, tak tada pokrenite:

```bash
# kompajlira docker sliku
./build_docker

# pokreće docker kontejner
./run_docker
```

## Licenca

```
Copyright (c) 2021 MEKOM d.o.o. Visoko - MIT Licenca

Daje se dozvola, bez naknade, bilo kojoj osobi koja ima kopiju ovog programa
i odgovarajuću dokumentaciju ("SOFTWARE"), da raspolaže SOFTWAREOM bez ikakvih
ograničenja, uključujući bez ograničenja prava na korištenje, kopiranje,
izmjenu, spajanje, objavljivanje, dijeljenje, podlicenciranje, i/ili prodaju
kopija SOFTWAREA, kao i da dozvoli osobama za koje je SOFTWARE namijenjen
da rade isto, u skladu sa sljedećim uslovima:

Obavještenja o autorskim pravima navedena iznad kao i ovo obavještenje odobrenja
imaju biti uključena u sve kopije ili bitne dijelove SOFTWAREA.

SOFTWARE SE DAJE "TAKAV KAKAV JESTE", BEZ GARANCIJA BILO KAKVE VRSTE,
EKSPLICITNIH ILI IMPLICITNIH, UKLJUČUJUĆI ALI NE OGRANIČAVAJUĆI SE
NA GARANCIJE MOGUĆNOSTI PRODAJE, PODESNOSTI ZA BILO KOJU NAMJENU,
ZAKONITOSTI ILI NEKRŠENJA TUĐIH PRAVA. NI U KOJEM SLUČAJU AUTORI
ILI VLASNICI AUTORSKIH PRAVA NEĆE BITI ODGOVORNI ZA BILO KAKAV ZAHTJEV,
ŠTETU ILI DRUGU OBAVEZU, BILO ZBOG UGOVORA, DELIKTA ILI DRUGAČIJE, NASTALOG IZ,
BEZ ILI U VEZI SA SOFTWAREOM ILI KORIŠTENJEM ILI RASPOLAGANJEM SOFTWAREOM.

---

Copyright (c) 2021 MEKOM d.o.o. Visoko - MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
