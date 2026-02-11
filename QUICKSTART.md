# ZustellApp - Schnellstart-Anleitung

## Voraussetzungen

1. **Python 3.8+** installiert
2. **Tesseract OCR** installiert:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-deu`
   - macOS: `brew install tesseract tesseract-lang`

## Installation & Start

### Automatische Installation (empfohlen)

**Windows:**
```bash
setup.bat
```

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

### Manuelle Installation

```bash
# Virtual Environment erstellen
python -m venv venv

# Aktivieren
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt

# MapView installieren
garden install mapview
```

## Demo-Daten erstellen

```bash
cd ZustellApp
python create_demo_data.py
```

Dies erstellt Beispiel-Pakete mit Wiener Adressen.

## App starten

```bash
cd ZustellApp
python main.py
```

## Verwendung

### 1. Startseite
- Zeigt alle Pakete in einer Liste
- "Scannen" Button öffnet die Kamera
- "Route anzeigen" zeigt die Karte

### 2. Scannen
- Kamera-Button (unten) macht ein Foto
- OCR erkennt automatisch die Adresse
- Adresse kann manuell korrigiert werden
- "Hinzufügen" speichert das Paket

### 3. Karte
- Zeigt alle Lieferpunkte als Marker
- "Route optimieren" berechnet die beste Route
- "Navigation starten" (in Entwicklung)

## Tipps

- Für beste OCR-Ergebnisse: Gute Beleuchtung, klare Schrift
- Geocoding benötigt Internet
- Bei vielen Paketen: Batch-Geocoding mit `geocode_packages.py`

## Troubleshooting

**Kamera funktioniert nicht:**
- Auf Desktop: Webcam erforderlich
- Berechtigungen prüfen

**OCR erkennt nichts:**
- Tesseract korrekt installiert?
- Pfad in PATH-Variable?

**Map zeigt nichts:**
- Internet-Verbindung prüfen
- Pakete geocodiert? (`geocode_packages.py`)

## Weitere Hilfe

Siehe vollständige Dokumentation in [README.md](README.md)
