# Dihur

To je orodje za masovno sintezno slik, ki posnemajo izgled starih parlamentarnih dokumentov. Razvit je bil na podlagi dokumentov iz parlamentarnih razprav Kranjske in SHS. Ker so skeni dokumentov dostikrat bledi, papir je lahko zmećkan, porumenel, tisk je viden na zadnji strani papirja in še česa, je OCR na danih dokumentih poln napak. S tem orodjem skušamo generirati podobne slike, ki pa imajo shranjeno izvorno besedilo (ground truth). Tako lahko sestavimo učno množico za učenje globokih LLMjev, ki bi lahko rezultate OCR besedila popravili. Vhodna besedila so pridobljena iz portala ParlaMint.

Opozorilo uporabniku: koda je zelo začetniška (moj prvi samostojen projekt), zato bo zagotovo v bližnji prihodnosti doživela prepis v boljšo obliko. Tudi ni nujno optimalna. Dokumentni sistem je zmeneden, zato je tukaj ta kratek Readme z razlago.

V root direktoriju je kar nekaj slik, ki prikazujejo primer rezultata orodja ter en .docx dokument, s pomočjo katerega so bile ustvarjene. Mapa ParlaMint vsebuje vso relevantno kodo.

```
ParlaMint
|  --> programi za postopek razvoja
|  --> t5
|  --> trainfiles_generating
```

Podmapa "programi za postopek razvoja" vsebuje dokaj nepomembno kodo, ki je bila uporabljena tekom začetka za testiranje in izvajanje OCR s pomočjo GoogleAPI. Pozor! - za ta korak je potreben Google APIKEY, ki ima neomejeno število uporab prve tri mesece, potem pa se uporaba zaračuna!

Direktno znotraj ParlaMint mape je skripta `transf.py`, s katero lahko poganjamo trening modela. 

Podmapa t5 vsebuje kodo povezano s treningom transformer modela mt5, nekatere datoteke učne množice (trainfiles_renamed) in rezultate testov na podatkih (podmape oblike test_*).

Glavni del, v katerem je koda za "orodje" za sintezo slik dokumentov, je v podmapi `trainfiles_generating`. Ta vsebuje vse potrebne podmape z zahtevanimi datotekami (fonti, ozadja, vodni_zig). Datoteka z najpogostejšimi ukazi je `ukazi_create_test_file.txt`.
Avtomatizirano generiranje slik poteka npr. z ukazom `python3 .\create_test_file.py "C:\Users\Student\Desktop\ParlaMint\trainfiles generating\ParlaMint-SI\2002" .\ozadja .\vodni_zig .\FillLayout3.py .\add_background.py .\image_processing.py 1`, ki pravzaprav vzame skripto `create_test_file.py`, prvi argument določi lokacijo s txt datotekami z vhodnimi besedili, določimo še lokacije za slike z ozadji, vodnimi žigi in lokacije skript za napolnjevanje Word predloge, converzijo v pdf in dodajanje ozadja ter končno za pretvorbo v slike ter manipulacijo in spremembe slik. Najrelevantenši je ravno ta zadnji del, ki je zapakiran v skripti `image_processing.py`. Ker vsak od teh programov sprejme točno določene argumente, jih že `create_test_file.py` pravilno izbere (naključno) in posreduje naprej. 
S programom `create_train_files.py` vzamemo v prejšnjem koraku pripravljene slike (imajo končnico `_modified.png`), poiščemo originalno besedilo in besedilo, ki ga na podlagi slik ustvari Google OCR. Dobimo dve datoteki, `*_original.txt` in `*_ocr.txt`.
Potem uprabimo še program `edlib_1.py`, s katerim ustvarimo končne datoteke, ki so nato vhod za trening modela. Podamo prej ustvarjeni datoteki kot argumenta (original in ocr), nato pa se s pomočjo knjižnice edlib besedila med seboj s primerjavo znakov poravnajo tako, da vsaka vrstica korespondira z isto vrstico med končnima datotekama tega programa. Nekaj vrstic je v tem procesu zavrženih. Določimo lahko, da kot rezultat vrnemo več opcij datotek - lahko so to posamezne povedi v eni vrstici (vezano na ločila), ali pa je v vsaki vrstici `n` besed in nismo vezani na povedi. Rezultat so datoteke s končnicami `_training_orig_{n}.txt` in `_training_ocr_{n}.txt`. V mapi je dodatno še kup programov, ki so namenjeni specifičnim popravkom. Npr. `automistakes.py` je namenjen ročnemu pokvarjanju pripravljenih trening datotek, da lahko opazujemo, če manualno dodajanje napak kakorkoli spremeni učinkovitost modela. `remove_parla_mint.py` iz besedilnih datotek odstrani stringe oblike `[ParlaMint ***]`, ki močno motijo OCR in rezultate, hkrati pa ta oblika besed ni relevantna za naš problem. Ostali programi so namenjeni evalvaciji modelov ali vmesnim korakom, ki so bili kasneje združeni v datoteke, opisane v tem odstavku. 
Podmapa `kranjska` vsebuje OCR rezultate dejanskih dokumentov, rezultati so ločeni glede na jezik vsebine (nekateri dokumenti mešajo slovenščino in nemščino). Podmapa `results` je posebej namenjena analizi modelov in primerjavi. Skripta`html_compare.py` omogoča prikaz razlik v dokumentu html, kjer so nato obarvane razlike med besedili. 
