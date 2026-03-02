# 🅿 Parking System

> A desktop vehicle parking management system built with **Python** and **CustomTkinter**.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/) [![UI: CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-green)](https://github.com/TomSchimansky/CustomTkinter) [![DB: SQLite](https://img.shields.io/badge/DB-SQLite-lightgrey)](https://www.sqlite.org/) [![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-informational)](https://paarthsiloiya.github.io/Parking-System/)

---

## ✨ Features

| Feature | Details |
|---------|---------|
| **Three simultaneous windows** | Entry, Exit, and Admin Control open together and stay in sync without manual refresh |
| **Vehicle Entry / Exit** | Register vehicles, auto-assign slots and tokens, generate bills instantly |
| **Automatic Billing** | Calculates fees from duration × ₹/hour rate per vehicle type |
| **Slot Management** | Multiple configurable floors with per-floor vehicle-type allotment |
| **Dynamic Pricing** | Set hourly rates per vehicle type at any time |
| **Records & Income** | Query parking records and income totals by date range |
| **Owner Panel** | Password-protected dashboard with full management controls |
| **Customisable UI** | Theme, font, accent colour, corner radius, and border width |

---

## 📦 Installation

### Prerequisites

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **pip** — included with Python

### 1. Clone the repository

```bash
git clone https://github.com/paarthsiloiya/Parking-System.git
cd Parking-System
```

### 2. Create and activate a virtual environment *(recommended)*

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python run.py
```

---

## 🖥️ Windows

The application opens **three independent windows** simultaneously, each sharing the same database:

| Window | Purpose |
|--------|---------|
| **Entry** | Register incoming vehicles — enter vehicle number, select type, get token and slot |
| **Exit** | Process departures — enter vehicle number to generate and display the bill |
| **Admin Control** | Owner login gate → management dashboard |

All windows are live-synced: a vehicle entry in the Entry window is visible in the Exit and Admin windows immediately, with no need to reload.

---

## 🚀 First-Run Setup

On the very first launch the app auto-creates:

| Resource | Details |
|----------|---------|
| `data/parking.db` | SQLite database — no server needed |
| `data/settings.json` | UI preferences |
| `data/credentials.json` | Owner login (default: `admin` / `admin123`) |
| `data/vehicle_options.json` | Enabled vehicle categories |
| Parking layout | 2 floors × 10 slots |
| Rates | All types at ₹0/hr — update in Admin Control |

**Recommended steps after first launch:**

1. Log into **Admin Control** (`admin` / `admin123`).
2. **Change Credentials** — set a secure username and password.
3. **Change Pricing** — set ₹/hour rates for each vehicle type.
4. *(Optional)* **Manage Parking Slots** — adjust floors and slots to match your facility.
5. *(Optional)* **Change Vehicle Options** — disable unused vehicle categories.

---

## 📖 Documentation

Full documentation is available at:

**[https://paarthsiloiya.github.io/Parking-System/](https://paarthsiloiya.github.io/Parking-System/)**

It includes:

- [Setup & Installation guide](https://paarthsiloiya.github.io/Parking-System/setup.html)
- [Usage guide](https://paarthsiloiya.github.io/Parking-System/usage.html)
- [Architecture overview](https://paarthsiloiya.github.io/Parking-System/architecture.html)
- [Full API reference](https://paarthsiloiya.github.io/Parking-System/api/index.html)

### Build the docs locally

```bash
pip install sphinx shibuya
sphinx-build -b html docs/ docs/_build/html
# Open docs/_build/html/index.html
```

---

## 🛠️ Technology Stack

| Component | Library |
|-----------|---------|
| GUI | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) |
| Database | SQLite (`sqlite3` — built-in) |
| Images | [Pillow](https://pillow.readthedocs.io/) |
| Date pickers | [tkcalendar](https://github.com/j4321/tkcalendar) |
| Docs | [Sphinx](https://www.sphinx-doc.org/) + [Shibuya theme](https://shibuya.lepture.com/) |

---

## ⚙️ Configuration

All configuration lives in `data/` as JSON files, created automatically on first run.

### `data/settings.json`

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `font_family` | string | `"Roboto"` | Font used across all windows |
| `font_size` | int | `14` | Base font size in points |
| `theme` | string | `"Dark"` | `"System"`, `"Light"`, or `"Dark"` |
| `accent_color` | string | `"blue"` | `"blue"`, `"green"`, or `"dark-blue"` |
| `corner_radius` | int | `12` | Widget corner radius |
| `border_width` | int | `0` | Widget border thickness |

### `data/credentials.json`

| Key | Description |
|-----|-------------|
| `username` | Owner username |
| `password_hash` | SHA-256 hex digest of the password |

Always change credentials through the app — do not edit `password_hash` manually unless you compute the SHA-256 digest yourself.

### `data/vehicle_options.json`

JSON array of active vehicle type strings. Full supported list:

```
Two Wheeler, Three Wheeler (Passenger), Three Wheeler (Freight),
Four Wheeler (Passenger), Four Wheeler (Freight), Mini Bus,
Bus, Mini Truck, Truck
```
