# Příprava na kurz
## Vytvoření pracovního prostoru 
Předpokladem je úspěšná instalace nástrojů a existence účtů, jak je popsáno [návodu `DAPYT_instalace-nastroju`](./resource/pdf/DAPYT_instalace-nastroju_1v2.pdf).

1. Vytvoř si na disku složku kurzu `DAPYTPCS20251013` se dvěma podsložkami
    ```
    DAPYTPCS20251013
    ├── resource   # tady budou sdíleny materiály kurzu a práce lektora
    └── working    # tohle je prostor pro Tvoji práci; složku propojíme s GitHub
    ```
    _Doporučení: nepoužívej složky synchonizované na Cloud (`GDrive`,`OneDrive`, apod.)_

2. Otevři si obě složky ve `VSCode` terminálu /nebo CLI svého OS/ a prověď následující kroky ...

## Připojení na `GitHub` lektora
Složku `resource` si napoj na projekt lektora na [`GitHub`](https://github.com/)   
**Před potvrzením následujících příkazů v terminálu nahraď bloky `<...>` skutečnými údaji**
```bash
git init
git remote add pcsda <keys.gitresource>
git pull pcsda main
```

## Stažení pracovních materiálů
1. Do složky `working` si z [`GitHubu`](https://github.com/) udělej klon kostry projektu (ve VScode terminálu /nebo CLI svého OS/)   
**Před potvrzením následujících příkazů v terminálu nahraď bloky `<...>` skutečnými údaji**  
**POZOR: tečka na konci následujícího přikazu je důležitá**
    ```bash
    git clone --depth 1 <keys.gitresource> .
    ```
2. Vymaž složku `.git`
3. Vytvoř si vlastní repo
    ```bash
    git init
    ```

## Příprava projektu ve VSCode
1. Po otevření složky `working` s **Tvým** projektem ve VSCode
    - nainstaluj doporučení `extensions`
    - restartuj VSCode
2. `Ctrl+Shift+P` vyber `Python: Create Environment`
    - pokud se zeptá, vyber správnou verzi Python
    - vyber prostředí `.venv`
    - zaškrtni použití `requirements.txt`
    - vyčkej na dokončení
3. Restartuj VSCode
4. Připrav si ve VSCode přístup do **Tvé** Neon databáze
5. Vytvoř v databázi uživatele `robot` a `student` postupným spuštěním SQL příkazů v souboru [resource/sql/db-grants.sql](resource/sql/db-grants.sql)
6. Vytvoř soubor [config/keys.yml](config/keys.yml),  
 nahraď bloky `<...>` v následujícím kódu skutečnými údaji   
 a zkopíruj si ho do nově vytvořeného souboru
```yaml
# `langlion` login nebo jina prezdivka
user: <`langlion` login nebo jina prezdivka>                 
# link zkopirovany z `NeonDB`
dburi: <link zkopirovany z `NeonDB`>
# Github repo `lektor`; URI včetně tokenu 
gitresource: <URI pro Github repo lektora>
# Github repo Tveho projektu; URI včetně tokenu
gitworking: <URI pro Tvoje Github repo>
```
7. spusť [tests/TestAppFunctions.py](tests/TestAppFunctions.py)
    - pokud to skončí "**OK**", je vyhráno
    - jiný výsledek vyřešíme individuálně

## Připojení ke *Tvému* `GitHubu`
1. Vytvoř ve svém GitHub nové *prázdné* `Repository` a token, pokud již nemáš hotovo
4. Následuje inicializace Tvého vlastního lokálního `Repository` a jeho propojení s tím na [`GitHubu`](https://github.com/)  
**Před potvrzením následujících příkazů v terminálu nahraď bloky `<...>` skutečnými údaji**
    ```bash
    git config user.name "<jmeno nebo prezdivka>"
    git config user.email "<email>"
    git remote add origin <keys.gitworking>
    git branch -M main
    git add .
    git commit -m "Initial commit"
    git push origin main
    ```

### V připadě potřeby aktualizace tokenu
```bash
git remote set-url origin https://<tvuj-novy-token>@github.com/<tvoje-repo>.git
```
