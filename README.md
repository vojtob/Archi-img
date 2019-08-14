# Archi-img : Doplnenie icon do obrázkov vyexportovaných z archi

Očakávaný postup je takýto:
1. **`exportImages.bat`** z Archimate modelu (`src\Architecture\model\*.archimate`) vygeneruje png súbory. Používa sa pri tom `autoit\exportImages.au3` ktorý simuluje klikanie v architool a generuje obrázky do `release\img_exported`. Preto musí byť pri tom otvorený model v architool. Pri vytváraní nového projektu treba premenovať v `exportImages.au3` názov archimatetool okna. 
1. **`addIcons.bat`** pridá do niektorých z týchto súborov ikonky. Zavolá sa `C:\Projects_src\Archi-img\lines.js` a ako parametre má cestu k projektu. Interne ešte potrebuje config súbor `src\Architecture\model\config.js` a popis súborov, do ktorých treba doplniť ikony
	1. Pre každý obrázok definovaný v popisnom súbore vygeneruje `release\img_lines\<subor>_lines.png`, kde sú naznačené všetky čiary identifikované v obrázku. To pomáha zistiť zarovnanie.
	2. Pre každý obrázok vygeneruje `release\img_lines\<subor>_rec.png`, kde sú označené všetky identifiované obdĺžniky s číslami, aby sa podľa toho dali doplniť ikony.
	3. Do obrázku doplní ikony (ak sú nejaké definované)
	4. Obrázok s doplnenými ikonami uloží do adresára
1. **`generateImages.bat`** vygenerovanie mermaid obrázkov
1. **`createSpec.bat`** Vytvorenie specifikacie 

  
## Popis adresárov

| Adresár                | Popis                                     | Môže sa zmazať?           |
| -----------------------|-------------------------------------------| ------------------------- |
| **src**                | Tu sú zdrojové veci                       | NIE, toto treba zálohovať |
| src/Architecture       | Architecture description                  | nie |
| src/Architecture/model | zdrojáky modelu                           | nie |
| src/Architecture/img   | zdrojáky obrázkov v mermaid               | nie |
| src/Architecture/specifikacia | Dokumentacia v md súboroch, z ktorej sa dajú generovať webové stránky alebo pdf dokumentácia | nie |
| src/res                | ikony, konfiguracia, ...                  | nie |
| **utils**                  | scripts na exportovanie, generovanie      | nie |
| **Architecture**       | Vygenerované, postprocessované, zkopírované súbory, výsledný tvar | áno, toto by sa malo dať celé vygenerovať |
| **release**            | Vygenerovaná dokumentácia, pomocné súbory pri generovaní, ... | áno |

## Atribúty obrázkov
```javascript
    { "fileName": "01-Business/01 Biznis Overview", "icons": [
        { "rec": 1, "x": "center", "y": "center", "size": 128, "iconName": "lifecycle.png"},
        { "rec": 2, "x": "left", "y": "top", "size": 96, "iconName": "notar.png"},
        { "rec": 3, "x": "right", "y": 0.7, "size": 96, "iconName": "businessoutcomes.png"}
    ]},
```

| Atribút                | Význam                                                  |
| -----------------------|-------------------------------------------------------- |
| fileName | Cesta k súboru v Architecture_temp, do tohto obrázka sa doplnia ikony |
| rec      | Číslo obdlžnika, z image_rec |
| x        | Kam sa umiestni ikona. Možné hodnoty sú left/center/right alebo koeficient napr. 0.2 |
| y        | Kam sa umiestni ikona. Možné hodnoty sú top/center/bottom alebo koeficient napr. 0.2 |
| size     | veľkosť v pixeloch, definuje to width (šírku), výška sa prispôsobí |


## Viacjazyčnosť
Ak chcem mať model v slovenčine aj angličtine, tak využijem properties jednotlivých elementov
SK_name je slovenský názov, EN_name anglický. Každý element má (v XML) atribút name, ktorý sa používa v obrázkoch.
Manipulovanie s názvami je nebezpečné, ľahko je to náchylné na to, že si prepíšem, čo som nechcel ... treba pred tým commitnúť.

| Príkaz | Význam |
|--------|--------|
| saveSK | Predpokladá, že som teraz používal model v slovenčine. Uloží všetky `element@name` do `@SK_name`. Takže predpokladá, že názvy sú po slovensky a zapamätá si ich do slovenského šuflíčka. |
| saveEN | Predpokladá, že som teraz používal model v angličtine. Uloží všetky `element@name` do `@EN_name`. Takže predpokladá, že názvy sú po anglicky a zapamätá si ich do anglického šuflíčka. |
| useSK | Je jedno, aké sú aktuálne názvy, či slovensky alebo anglicky. Hovorím, že chcem prejsť do slovenčiny a tak vyberie slovenský šuflík a všetky názvy si nastaví podľa neho. Do `element@name` nastaví `@SK_name`. |
| useEN | Je jedno, aké sú aktuálne názvy, či slovensky alebo anglicky. Hovorím, že chcem prejsť do anlgičtiny a tak vyberie anglický šuflík a všetky názvy si nastaví podľa neho. Do `element@name` nastaví `@EN_name`. |

Ak sa chcem prepnúť do angličtiny, tak by som mal 
* saveSK aby som nestratil slovenské názvy, ktoré som upravil
* useEN aby sa načítali anglické názvy

A podobne pri prechode z angličtiny do slovenčiny saveEN, useSK
