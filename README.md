# Datová Analytika
**Praha Coding School** (https://prahacoding.cz/)  
**Martin Rosický** <martinr.prahacoding@gmail.com>  
Video záznamy z lekcí [na Youtube](<https://www.youtube.com/playlist?list=PLmiFROzBONlTTXRpqpPD9UbNsRDsH0dDK>)

## O kurzu
Kurz navržený pro ty, kteří chtějí rozšířit svou současnou roli o znalosti v oblasti analýzy a vizualizace dat. Naučíme se vyvinout ucelenou, opakovaně použitelnou aplikaci k manipulaci a analýze data za pomocí jazyka Python a jiných volně dostupných nástrojů od datábází přes modely umělé inteligence a strojového učení.

### Co se naučíš?
- základní programové konstrukce Python
- čtení a zápis dat v různých formátech včetně Big Data
- manipulaci s daty funkcemi knihovny Pandas i s využitím ML
- export výstupů do analytických systémů a HTML/PDF
- ošetření chyb a logování běhu programu
- ovládání aplikace z příkazové řádky a konfiguračního souboru
- vytvoření spustitelného balíčku

## Co tu najdeš?
1. složky obsahují
    - připravené "prezentace" [resource](./resource/pdf)
    - pracovní materiály, se kterými budeme pracovat během kurzu
    - **Tvůj** projekt
1. budeme pracovat se dvěma složkami propojenými na [`GitHub`](https://gihub.com)
    - složka lektora: prostřednictvím Git budeš mít přístup ke všemu, co lektor tvoří
    - **Tvoje** vlastní pracovní složka: Git bude zálohou **Tvé** práce a může být i nástrojem pro její sdílení
1. tyto složky a soubory jsou fyzicky uložené a disku **Tvého** počítače; jsou tedy:
    - přístupné kdykoliv
    - můžeš s nimi pracovat jako s jinými soubory v počítači
1. návod na uvedení v život je v souboru [INSTALL.md](./INSTALL.md)

## Zdroje na Internetu
### Linky pro stažení potřebných nástrojů
- [`VSCode`](https://code.visualstudio.com/download) - integrované vývojové prostředí IDE
- [`Git`](https://git-scm.com/download) - programátorský nástroj pro sledování verzí zdrojového kódu a týmovou spolupráci
- [`Python`](https://www.python.org/downloads/) - programovací jazyk hojně využívaný datovými analytiky
- [`Tableau Public Desktop`](https://www.tableau.com/products/desktop/download) - free verze nástroje pro grafickou prezentaci a analýzu dat

### On-line nástroje
- [`GitHub`](https://gihub.com) - programátorský cloud pro ukládání zdrojových kódů, sledování verzí a týmovou spolupráci
- [`Neon`](https://neon.tech/) - Free on-line (serverless) Postgres SQL databáze 
- [`Grafana`](https://grafana.com/) - analytický a vizualizační nástoj zaměřený prezentaci dynamických dat s přímým připojením do DB
- [`Tableau Public`](https://public.tableau.com/app/discover) - free verze analytického a vizualizačního nástoje se zaměření na stati zaměřený prezentaci statických/business dat
- [`Regex`](https://regex101.com/) - testovací stránka pro regulární výrazy
- [`SQL lines`](https://www.sqlines.com/home) - nástroj pro převod schémat a dat mezi SQL databázemi

### On-line dokumentace
#### [`Pandas`](https://pandas.pydata.org/)
- [User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [`DataFrame` API](https://pandas.pydata.org/docs/reference/frame.html)
- [SQLAlchemy](https://www.sqlalchemy.org/) - nástroj pro přístup k SQL databázím
#### [`scikit-learn`](https://scikit-learn.org/1.5/user_guide.html)
- [Algoritmy "s učitelem"](https://scikit-learn.org/1.5/modules/multiclass.html) - učí se na známých výsledcích
- [Algoritmy "bez učitele"](https://scikit-learn.org/1.5/unsupervised_learning.html) - pro celkový pohled na data
- [Rozcestník agoritmů](https://scikit-learn.org/1.5/machine_learning_map.html)
- [`Feature selection`](https://scikit-learn.org/1.5/modules/feature_selection.html#feature-selection) - výběr `feature` /parametrů/, které nejlépe korelují s očekávanými výsledky
- [Nalezení "správných parametrů" algoritmu](https://medium.com/dvt-engineering/hyper-parameter-tuning-for-scikit-learn-ml-models-860747bc3d72)


## Tipy a triky

### Git
- `Commit and Push` svého projeku po každé větší změně nebo na konci tréninkového dne
  - tohle je užitečné nejen pro sledování změn, ale je to **Tvoje** záloha pro případ pádu počítače
- `Pull` lektorského projektu vždy, když s ním chceš pracovat
  - v případě chyby `Pull` použij `Branch -> Rebase` ... ignoruje všechny lokální úpravy a stáhne verzi z GitHub
  - pokud předchozí akce nedopadne dobře, podívej se do seznamu změn v `Source Control` a zruš všechny změny v souborech

### Python
- vytvoření virtuálního prostředí v CLI:
  ```
  cd <složka-projeku>
  <cesta-k-verzi-python>/python -m venv .venv
  ```
- aktivace virtuálního prostředí v CLI:
  - Windows PowerShell `<složka-projeku>: .\.venv\Scripts\activate`
  - Linux/MacOS: `<složka-projeku>$ source ./.venv/bin/activate`
- ověření, že je virtuální prostředí aktivní je možné použít příkaz `pip -V`, který vypíše cestu, ze které je `pip` volán
- instalace knihoven `(.venv) <složka-projeku>: pip install <jmeno-knihovny>`
- upgrade `pip`: `python -m pip install --upgrade pip`
- vytvoření spustitelného balíčku `pyinstaller -n analyzer --onefile -p .\analyzer\ .\analyzer\__main__.py`
- MacOS: [instalace certifikátů pro https](https://matduggan.com/til-python-3-6-and-up-is-broken-on-mac/):  
  v terminálu napiš příkaz: `/Applications/Python\ 3.13/Install\ Certificates.command`
- registrace přístupu do databáze pro robota
    ``` python
    import requests
    data = {'conn_name': <langlion-loginname>, 'conn_string': <neon-robot-connection>}
    requests.post('https://development.techniarch.com/pcsda/robot.php?register',data=data)
    ```
- seznam databází robotů https://development.techniarch.com/pcsda/robot.php?dbs=psycopg2

#### Pro hračičky
pár námětů navazujících na to, co se probírá v kurzu:
- pohrajte si s rodinkou ... doplňte další členy, doplňte jim věk a spočítejte si průměrné věky celkem, v rámci generace a tak
- ČNB kurzy ... přidejte si další měny, spočítejte průměrný kurz za celé období, spočítejte kurzy mezi měnami; upravte kód tak, aby umožnil zvolit časové období
- [hry s kostkami](https://www.proasist.cz/blog/hraci-kostky-aneb-nekonecno-zabavy/) ... zajímavé by mohly být například hry: Oči, Zlá trojka, Třikrát paš, Cesta do Ameriky

Nezapomeň, že je potřeba nejdříve přemýšlet a pak teprve kódovat ;-)

### PowerShell
- povolení spouštění skriptů: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force;`
- zabránění zavření okna při spuštění `exe` souboru z win Exploreru - vytvoř `bat` soubor:
```
	@echo off
	<exe-soubor>
	pause
```

