# Expense Tracker

Eine lokale Webanwendung, mit der Einnahmen und Ausgaben erfasst und in einer SQLite-Datenbank gespeichert werden.

## Funktionen

- Einnahmen und Ausgaben erfassen
- Kategorien passend zur Buchungsart auswählen
- Beträge und Kategorien serverseitig validieren
- Buchungen dauerhaft in SQLite speichern
- Buchungen mit deutschem Datums- und Währungsformat anzeigen
- JSON-API für Buchungen bereitstellen
- Funktionen mit pytest testen

## Voraussetzungen

- Python 3.10 oder neuer

## Installation

Die Befehle in PowerShell im Projektordner ausführen:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Anwendung starten

```powershell
python -m uvicorn app.main:app --reload
```

Die Anwendung ist anschließend unter http://127.0.0.1:8000 erreichbar. Mit `Ctrl+C` wird der Server beendet.

## Tests ausführen

```powershell
python -m pytest
```