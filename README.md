📌 Siemens camera connect – projekt

Projekt uporablja OpenCV za zajem video toka in zaznavo barv (HSV maske), da določi orientacijo nalepk na kosih. Rezultati se prikažejo v grafičnem vmesniku (Tkinter). Pošljejo se v Siemens PLC preko knjižnice snap7, da lahko ostali deli sistema zagrabijo in ločujejo kose.

Glavne funkcionalnosti

🔎 Pregled dostopnih kamer (camera_detect.py)

🖼 GUI z video prikazom, maskami in statusnim oknom
(kamera_senzor.py, camera_senzor_connect.py, camera_senzor_connect_v1.py)

🔗 Povezava in zapis v Siemens PLC
(simens_conect.py, simens_connect1.py)

🛠 Helper funkcije za branje/pisanje v PLC
(primeri in reference v simens_connect1.py)

Struktura datotek
camera_detect.py → test, kateri indeksi kamer so dostopni
kamera_senzor.py → GUI-only (prikaz kamere in maske, brez PLC)
camera_senzor_connect.py → GUI + detekcija barv + zapis v PLC (int vrednosti)
camera_senzor_connect_v1.py → podobno kot zgoraj, uporablja boolean pisanje
simens_conect.py → preprost test povezave in branja iz PLC
simens_connect1.py → helper funkcije (read/write Bool, memory)

Kako deluje

Program zajame sliko iz kamere (cv2.VideoCapture).
Pretvori frame v HSV in ustvari masko za ciljno barvo (modra, rdeča, bela).
Uporabi morfološke operacije in konture za iskanje objektov ter izračun težišča.
Na podlagi zaznane barve posodobi status v GUI-ju in pošlje ustrezno vrednost v PLC (če je konfigurirano).

Konfigurabilni parametri
IP naslovi PLC: v skriptih trenutno hard-coded (npr. 192.168.0.1)
DB in offseti: db_number, start_offset, bit_offset
Index kamere: cv2.VideoCapture(0) – spremenite 0 po potrebi
Min area: min_area v find_color, določa najmanjšo zaznano konturo

Predpogoji
Python 3.8 ali novejši
Na Windows priporočeno virtualno okolje (venv ali conda)
Zahtevane knjižnice
requirements.txt vsebuje vse odvisnosti. Ključne so:
opencv-python
numpy
pillow
python-snap7
tqdm

Namestitev (PowerShell)
# Ustvarite in aktivirajte virtualno okolje
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Namestite odvisnosti
pip install -r .\requirements.txt

Kako zagnati
Hiter test kamer
python .\camera_detect.py

GUI brez PLC (lokalni prikaz)
python .\kamera_senzor.py


GUI s povezavo na PLC (prilagodite IP/DB v skripti)
python .\camera_senzor_connect.py
# ali
python .\camera_senzor_connect_v1.py

Konfiguracija
V skripti spremenite:
plc.connect('192.168.0.1', 0, 1) → nastavite IP, rack, slot vašega PLC
db_number, start_offset, bit_offset → DB in bita za zapis
cv2.VideoCapture(0) → indeks kamere
min_area → prag velikosti kontur

Odpravljanje napak
Kamera ne deluje
preverite, če jo uporablja drug program
testirajte z različnimi indeksi (0, 1, 2 …) preko camera_detect.py
Težave s snap7
lahko zahtevane binarne komponente (če pip install python-snap7 ne uspe)
preverite GET/PUT dovoljenja v PLC
DB naj bo neoptimiziran
vedno uporabljajte try/except in finally za varno disconnect()
Rdeča barva v HSV
potreben je dvojen interval:

[0,120,70] – [10,255,255]

[170,120,70] – [180,255,255]

Predlagane izboljšave
Premik PLC logike v ločen modul (plc_wrapper.py)
Odstranitev connect() ob samem importu modulov
Dodajanje konfiguracijske datoteke (config.json ali .env)
Združitev camera_senzor_connect.py in _v1


Datoteke v repozitoriju
README.md → opis projekta in navodila
requirements.txt → zahteve