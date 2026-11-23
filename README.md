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

## Technologien

- Python und FastAPI für Backend und API
- SQLite für die Datenspeicherung
- Jinja2, HTML, CSS und JavaScript für die Benutzeroberfläche
- pytest für automatisierte Tests

## API-Endpunkte

| Methode | Pfad | Beschreibung |
|---|---|---|
| `GET`| `/transactions`| Gibt Buchungen als JSON zurück|
| `POST`| `/transactions`| Speichert eine Buchung aus JSON; der Betrag wird in Cent erwartet|
| `POST`| `/transactions/form`| Speichert eine Formularbuchung und leitet zur Startseite zurück|

### Beispiel: Buchung als JSON anlegen

An den Endpunkt POST /transactions wird ein JSON-Objekt gesendet:

```json
{
    "amount": 2500,
    "transaction_type": "expense",
    "category": "Lebensmittel",
    "date": "2026-11-22",
    "description": "Wocheneinkauf"
}
```

Der Betrag wird in Cent angegeben: `2500` entspricht `25,00 €`. Bei Erfolg antwortet die API mit Status `201`:

```json
{
    "message": "Transaktion erfolgreich gespeichert!"
}
```

## Projektstruktur

```text
app/
├── main.py
├── database.py
├── schemas.py
├── services.py
├── routers/
│   └── transactions.py
├── templates/
│   └── index.html
└── static/
│   ├── category-filter.js
│   └── style.css

tests/
├── test_api.py
├── test_database.py
└── test_pages.py

```

- `main.py` startet FastAPI und zeigt die Website an.
- `database.py` verwaltet die SQLite-Datenbank.
- `routers/` enthält die Transaktions-Endpunkte.
- `templates/` und `static/` enthalten die Oberfläche.
- `tests/` enthält die automatisierten Tests.