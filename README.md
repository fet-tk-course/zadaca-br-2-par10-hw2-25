[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wxDq4rbD)
# Zadaća 2 - REST API aplikacija

## O projektu

Kao domenu naše aplikacije odabrali smo muzičku industriju. S obzirom na to da u toj domeni imamo raznolike mogućnosti za kreiranje potrebnih endpointa, odlučili smo analizirati relaciju albumi/pjesme. Student A se bavi albumima, dok se student B bavi pjesmama.

## Tim

- **Student A**: Tahira Zukić - resurs: `/Albumi`
- **Student B**: [Ime Prezime] - resurs: `/resursi_b`

## Instalacija i pokretanje

### Preduvjeti

- Python 3.10 ili noviji
- pip

### Koraci

1. Klonirajte repozitorij:
```bash
git clone <url-repozitorija>
cd <naziv-repozitorija>
```

2. Kreirajte virtuelno okruženje:
```bash
python -m venv venv
```

3. Aktivirajte virtuelno okruženje:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instalirajte zavisnosti:
```bash
pip install -r requirements.txt
```

5. Pokrenite aplikaciju:
```bash
uvicorn main:app --reload
```

6. Otvorite browser na adresi: `http://localhost:8000/docs`

## API Endpointi

### Resurs A: `/Albumi`

| Metoda | Ruta | Opis |
|--------|------|------|
| GET | `/Albumi` | Lista svih resursa (sa query filterom) |
| GET | `/Albumi/{id}` | Dohvatanje resursa po ID-u |
| POST | `/Albumi` | Kreiranje novog resursa |
| PUT | `/Albumi/{id}` | Potpuna zamjena resursa |
| PATCH | `/Albumi/{id}` | Djelimično ažuriranje resursa |
| DELETE | `/Albumi/{id}` | Brisanje resursa |

**Primjer zahtjeva:**
```bash
# Kreiranje novog resursa
curl -X POST "http://localhost:8000/resursi_a" \
  -H "Content-Type: application/json" \
  -d '{"polje1": "vrijednost", "polje2": 123}'
```
### Resurs A: Odbrana zadaće
**Zadatak 1:**
U zadatku br. 1 kreirani su validatori za polja title, price i release_year. Za polje title, validator je da to polje ne može biti prazno. Polje release_year ne smije biti tipa float, dok price ne smije biti veća od 10000. Kreirana je nova klasa koja sadrži samo navedena polja. Validatori su testirani u POST endpointu. Greške koje potencijalno mogu nastati su HTTP_404_NOT_FOUND, HTTP_409_CONFLICT i sl. 
Primjer zahtjeva: curl -X POST "http://localhost:8000/resursi_a" \
  -H "Content-Type: application/json" \
  -d '{"polje1": "vrijednost", "polje2": 123}'.



### Resurs B: `/resursi_b`

[Analogno kao za Resurs A]

## Korištenje AI alata

### Alat: Google Gemini AI
**Model:** 

**Primjer 1:**
- **Prompt:** Potrebno implementirati GET endpoint sa query parametrima. Prilažem ti kod i na osnovu njega mi daj prijedlog kako da poboljšam isti, bez pisanja if statementa za svaki zahtjev, uključujući edge cases.
- **Kako je pomoglo:** Unaprijedilo je moj moj kod. Kod izgleda elegantnije i razumljiv je za čitanje. Nema if statementa, koji jesu korisni za čitanje i razumijevanje koda, ali nisu estetični vizuelno. 
- **Prilagodbe:** Kod sam minimalno prilagodila svojim mogućnostima razumijevanja.

**Primjer 2:**
- **Prompt:** [Npr. "Implementiraj PATCH endpoint sa exclude_unset=True"]
- **Kako je pomoglo:** [Opis]
- **Prilagodbe:** [Opis]

## Napomene

[Dodatne napomene specifične za vašu implementaciju]