# Archi-img
Doplnenie icon do obrazkov vyexportovanych z archi

Očakávaný postup je takýto:
1. C:\Projects_src\or\Architecture_src\utils\exportImages.bat sa z Archimate modelu (C:\Projects_src\or\Architecture_src\model\orsr.archimate) vygenerujú png súbory
2. Niektoré z týchto súborov chcem obohatiť o ikonky. Na to slúži C:\Projects_src\or\Architecture_src\utils\addIcons.bat, ktorý zavolá C:\Projects_src\Archi-img\lines.js. Ten potrebuje config súbor (C:\Projects_src\or\Architecture_src\utils\config\config.js) a popis súborov, do ktorých treba doplniť ikony
3. lines.js urobí:
  1. pre každý definovaný súbor vygeneruje <subor>_lines.png, kde sú naznačené všetky čiary identifikované v obrázku. To pomáha zistiť zarovnanie. Súbory skončia v adresári Architecture_temp/
  2. pre každý definovaný súbor vygeneruje <subor>_rec.png, kde sú označené všetky identifiované obdĺžniky s číslami, aby sa podľa toho dali doplniť ikony. Súbory skončia v adresári Architecture_temp/
  3. Do obrázku doplní ikony (ak sú nejaké definované)
  4. Obrázok s doplnenými ikonami uloží do adresára
