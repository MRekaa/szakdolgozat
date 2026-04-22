# Python alapú grafikus alkalmazásfejlesztés – Virtuális kémiai labor

Oktatási célú, Python alapú 2D-s játékalkalmazás, amely a kémiai reakciók tanulását támogatja egy interaktív virtuális laboratóriumi környezetben.

A projekt célja, hogy a diákok játékos formában gyakorolhassák a kémiai reakciókat, anyagok kombinálását és új vegyületek előállítását.

---

## Projekt célja

Az alkalmazás egy digitális tanulási eszköz, amely:

- támogatja a kémiai reakciók vizuális megértését
- interaktív módon segíti a tanulást
- biztonságos laboratóriumi környezetet szimulál
- játékos formában motiválja a felhasználókat

A felhasználó különböző anyagokat és eszközöket helyezhet el a játéktéren, ahol azok reakcióba léphetnek egymással.

---

## Fő funkciók

- Drag-and-drop alapú objektumkezelés
- Anyagok és eszközök kiválasztása hotbarból
- Automatikus reakciófelismerés
- Új anyagok létrehozása
- Keresőrendszer receptekhez
- Item törlés kuka zónával
- Reszponzív felhasználói felület
- MySQL alapú adatkezelés

---

## Használt technológiák

- **Python 3.10**
- **Pygame**
- **MySQL**
- **mysql-connector-python**
- **pytest**
- **Git / GitHub**

---

## Telepítés

### 1. Projekt klónozása

```bash
git clone https://github.com/MRekaa/szakdolgozat.git
cd szakdolgozat
```

### 2. Virtuális környezet létrehozása

```bash
python -m venv venv
```

### 3. Virtuális környezet aktiválása

Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

### 4. Függőségek telepítése

```bash
pip install pygame mysql-connector-python pytest
```

vagy

```bash
pip install -r requirements.txt
```

---

## Adatbázis beállítása

A projekt MySQL adatbázist használ.

Hozz létre egy `labor` nevű adatbázist, majd futtasd a mellékelt SQL fájlt:

```sql
database.sql
```

Alapértelmezett kapcsolat:

- host: `localhost`
- user: `root`
- password: *(üres)*
- database: `labor`

Szükség esetén módosítsd a kapcsolatot itt:

```python
src/dataBase.py
```

---

## Program futtatása

```bash
python src/main.py
```

Sikeres indítás után megjelenik a **Labor** nevű Pygame ablak.

---

## Játékmenet

1. Válassz anyagot vagy eszközt a hotbarból
2. Húzd a játéktérre
3. Helyezd más elemek közelébe
4. Kompatibilis elemek esetén reakció indul
5. Új anyag jön létre
6. A keresőrendszer segít receptek keresésében

---

## Tesztelés

Automatikus tesztek futtatása:

```bash
pytest
```

Tesztelt funkciók:

- reakciókezelés
- receptkeresés
- kuka működése
- item törlés
- integrációs reakciótesztek

---

## Példa reakció

```text
H2 + O2 → H2O
```

---

## Fejlesztési cél

A projekt elsődlegesen oktatási célú alkalmazásként készült szakdolgozati projekt keretében.

---

## Szerző

**Mészáros Réka**  
Programtervező informatikus BSc  
Eszterházy Károly Katolikus Egyetem

---

## Témavezető

**Kovács Ádám**  
Tanársegéd

---

## Licenc

Ez a projekt oktatási célra szabadon felhasználható.
