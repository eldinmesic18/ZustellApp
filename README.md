# ZustellApp

Eine mobile Anwendung für Postboten zur Optimierung der Paketzustellung mit OCR-Scanning, Routenplanung und Kartenvisualisierung.

## Features

- 📸 **OCR-Scanning**: Automatisches Erkennen von Adressen durch Kamera-Scan
- 🗺️ **Kartenintegration**: Visualisierung aller Lieferadressen auf einer interaktiven Karte
- 🚀 **Routenoptimierung**: Automatische Berechnung der optimalen Lieferroute (TSP-Algorithmus)
- 📝 **Notizen**: Speichern von Notizen für spezifische Adressen
- 📦 **Paketverwaltung**: Verwaltung von Paketen und Briefen mit Status-Tracking

## Technologie-Stack

- **Framework**: KivyMD (Cross-Platform Mobile Development)
- **Datenbank**: SQLite
- **OCR**: Tesseract OCR
- **Karten**: kivy-garden.mapview (OpenStreetMap)
- **Geocoding**: Nominatim (OpenStreetMap)
- **Routenoptimierung**: Scipy (TSP-Solver)

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- Tesseract OCR installiert auf dem System

#### Tesseract Installation

**Windows:**
```bash
# Download von: https://github.com/UB-Mannheim/tesseract/wiki
# Nach Installation Pfad zu PATH hinzufügen
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-deu
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

### App Installation

1. Repository klonen oder herunterladen
2. Abhängigkeiten installieren:

```bash
cd ZustellApp
pip install -r requirements.txt
```

3. MapView installieren:

```bash
garden install mapview
```

## Verwendung

### App starten

```bash
cd ZustellApp
python main.py
```

### Pakete geocodieren

Bevor die Routenoptimierung funktioniert, müssen die Adressen geocodiert werden:

```bash
python geocode_packages.py
```

### Workflow

1. **Startseite**: Übersicht aller Pakete
2. **Scannen**: Kamera öffnen und Adresse scannen
   - Foto aufnehmen
   - OCR erkennt automatisch die Adresse
   - Adresse manuell korrigieren falls nötig
   - Paket zur Liste hinzufügen
3. **Route anzeigen**: Karte mit allen Lieferpunkten
   - Route optimieren für effiziente Zustellung
   - Marker zeigen alle Lieferadressen

## Projektstruktur

```
ZustellApp/
├── main.py                 # Hauptanwendung
├── database.py            # Datenbank-Verwaltung
├── ocr_engine.py          # OCR-Funktionalität
├── routing.py             # Routenoptimierung
├── geocoding.py           # Adress-zu-Koordinaten Konvertierung
├── geocode_packages.py    # Hilfsskript für Batch-Geocoding
├── ui/
│   └── main.kv           # UI-Definition (KivyMD)
├── captures/             # Gespeicherte Scans
├── requirements.txt      # Python-Abhängigkeiten
└── zustellapp.db        # SQLite-Datenbank
```

## Datenbank-Schema

### Packages
- id, address, status, type, notes, latitude, longitude, timestamp

### Routes
- id, name, created_at

### Address_Notes
- id, address, note, created_at

## Entwicklung

### Testdaten hinzufügen

```python
from database import Database

db = Database()
db.add_package("Hauptstraße 1, 1010 Wien", type="package", notes="Testpaket")
db.add_package("Mariahilfer Straße 10, 1060 Wien", type="letter")
db.close()
```

### Geocoding testen

```python
from geocoding import Geocoder

geocoder = Geocoder()
coords = geocoder.geocode("Stephansplatz 1, 1010 Wien")
print(coords)  # (48.208493, 16.373129)
```

## Bekannte Einschränkungen

- OCR-Genauigkeit hängt von der Bildqualität ab
- Geocoding benötigt Internetverbindung
- Nominatim API hat Rate-Limits (1 Request/Sekunde)
- MapView funktioniert am besten auf mobilen Geräten

## Zukünftige Erweiterungen

- [ ] GPS-Integration für Echtzeit-Navigation
- [ ] Offline-Karten
- [ ] Barcode/QR-Code Scanning
- [ ] Unterschriften-Erfassung
- [ ] Cloud-Synchronisation
- [ ] Multi-User Support

## Lizenz

Dieses Projekt ist für Bildungszwecke erstellt.

## Autor

Entwickelt für die Optimierung der Paketzustellung.
