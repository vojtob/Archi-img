# Archi-img : Doplnenie icon do obrázkov vyexportovaných z archi

Očakávaný postup je takýto:
1. Pomocou `utils\exportImages.bat` sa z Archimate modelu (`Architecture_src\model\*.archimate`) vygenerujú png súbory. Používa sa pri tom `utils\autoit\exportImages.au3` ktorý simuluje klikanie v architool a generuje obrázky do `Architecture_temp\exported`. Preto musí byť pri tom otvorený model v architool. Pri vytváraní nového projektu treba premenovať v `exportImages.au3` názov archimatetool okna. 
2. Niektoré z týchto súborov chcem obohatiť o ikonky. Na to slúži `utils\addIcons.bat`, ktorý zavolá `C:\Projects_src\Archi-img\lines.js` a ako parametre má cestu k projektu a cestu kam má exportovať finálne obrázky. Interne ešte potrebuje config súbor `Architecture_src\model\config.js` a popis súborov, do ktorých treba doplniť ikony
	1. Pre každý obrázok definovaný v popisnom súbore vygeneruje `Architecture_temp\lines\<subor>_lines.png`, kde sú naznačené všetky čiary identifikované v obrázku. To pomáha zistiť zarovnanie.
	2. Pre každý obrázok vygeneruje `Architecture_temp\lines\<subor>_rec.png`, kde sú označené všetky identifiované obdĺžniky s číslami, aby sa podľa toho dali doplniť ikony.
	3. Do obrázku doplní ikony (ak sú nejaké definované)
	4. Obrázok s doplnenými ikonami uloží do adresára

  
## Popis adresárov

| Adresár                | Popis                                     | Môže sa zmazať?           |
| -----------------------|-------------------------------------------| ------------------------- |
| **Architecture_src**   | Tu sú zdrojové veci                       | NIE, toto treba zálohovať |
| Architecture_src/memos | Lightweight Architecture Decision Records | nie |
| Architecture_src/model | zdrojáky modelu                           | nie |
| Architecture_src/utils | nástroje na exoportovanie, generovanie    | nie |
| Architecture_src/img   | obrázky, ktoré nie sú z modelu, tieto sa budú iba kopírovať do výslednej štruktúry | nie |
| **Architecture**       | Vygenerované, postprocessované, zkopírované súbory, výsledný tvar | áno, toto by sa malo dať celé vygenerovať |
| Architecture/01-Business, 02-Application, 03-Technology | vygenerované obrázky s doplnenými ikonami | áno, dajú sa nanovo vygenerovať |
| **Architecture_temp**  | Pomocné súbory pri generovaní             | áno |
