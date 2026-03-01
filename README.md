# Parking System

A desktop parking management system built with Python and CustomTkinter.

## Features

- **Vehicle Entry / Exit** — Register vehicles, assign slots, generate tokens automatically
- **Automatic Billing** — Calculate parking fees based on duration and per-hour rates
- **Slot Management** — Multiple floors with configurable slot counts
- **Vehicle Type Control** — Enable or disable vehicle categories
- **Dynamic Pricing** — Set per-hour rates per vehicle type
- **Records & Income** — Query parking records and income by date range
- **Owner Panel** — Password-protected management dashboard
- **Customizable UI** — Theme, fonts, accent colour, corner radius, and more

---

## First-Time Setup

### Prerequisites

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **pip** — Included with Python

### 1. Clone & enter the project

```bash
git clone <repo-url>
cd "Parking System"
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the app

```bash
python run.py
```

On the very first launch, the app automatically creates:

| Item | Details |
|------|---------|
| **Database** | `data/parking.db` — SQLite, no server needed |
| **Settings** | `data/settings.json` — UI preferences |
| **Credentials** | `data/credentials.json` — owner login (hashed) |
| **Vehicle options** | `data/vehicle_options.json` — active vehicle types |
| **Parking layout** | 2 floors × 10 slots each |
| **Rates** | All vehicle types at ₹0 — update in *Owner Panel → Change Pricing* |

### 5. Recommended first-run steps

1. Log into the **Owner Panel** (default: `admin` / `admin123`).
2. Open **Change Credentials** and set your own username and password.
3. Open **Change Pricing** and set per-hour rates for each vehicle type.
4. (Optional) Open **Manage Parking Slots** to adjust the number of floors / slots.
5. (Optional) Open **Vehicle Options** to disable vehicle types you don't need.

---

## Usage Guide

### Entry workflow

1. Click **ENTRY** on the main menu.
2. Type the vehicle number and select a vehicle type.
3. Click **Enter Vehicle** — a token number and slot are assigned automatically.
4. Note the token number for the vehicle owner.

### Exit workflow

1. Click **EXIT** on the main menu.
2. Type the vehicle number and click **Generate Bill**.
3. A bill dialog shows entry/exit times, slot, and total amount.
4. The slot is freed automatically.

### Owner Panel

Access via **OWNER** on the main menu → enter credentials.

| Option | What it does |
|--------|-------------|
| **Change Credentials** | Update owner username and/or password |
| **View Records** | Browse parking records by date range |
| **Delete Records** | Remove records (all, by date, or by vehicle) |
| **Change Vehicle Options** | Enable/disable vehicle types |
| **View Income** | See total income for a date range |
| **Change Pricing** | Set per-hour rate for each vehicle type |
| **Manage Parking Slots** | Add/remove floors and slots, allot vehicle types to floors |
| **Settings** | Change font, theme, accent colour, and more |

### Settings shortcut

The **Settings ⚙** button on the top-right of the main menu opens the settings screen directly without needing to go through the Owner Panel.

---

## Customizable Variables

All configuration lives in the `data/` directory as JSON files. They are created automatically on first run and can be edited in the app or directly in the files (restart required for manual edits).

### `data/settings.json` — UI preferences

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `font_family` | string | `"Roboto"` | Font used throughout the UI |
| `font_size` | int | `14` | Base font size in pixels |
| `theme` | string | `"Dark"` | Appearance mode: `"System"`, `"Light"`, or `"Dark"` |
| `accent_color` | string | `"blue"` | Colour theme: `"blue"`, `"green"`, or `"dark-blue"` |
| `corner_radius` | int | `12` | Button / input corner radius |
| `border_width` | int | `0` | Button / input border width |

Change these from **Settings** in the app, or edit the file and restart.

### `data/credentials.json` — Owner login

| Key | Type | Description |
|-----|------|-------------|
| `username` | string | Owner username |
| `password_hash` | string | SHA-256 hash of the password |

Change via **Owner Panel → Change Credentials**. Do not manually edit `password_hash` unless you compute the SHA-256 hex digest yourself.

### `data/vehicle_options.json` — Active vehicle types

A JSON array of enabled vehicle type strings. The full list of supported types:

```
Two Wheeler, Three Wheeler (Passenger), Three Wheeler (Freight),
Four Wheeler (Passenger), Four Wheeler (Freight), Mini Bus,
Bus, Mini Truck, Truck
```

Change via **Owner Panel → Change Vehicle Options**.

### Pricing & Slots

These are stored in the SQLite database (`data/parking.db`) and should be changed through the app:

- **Pricing** — *Owner Panel → Change Pricing* — set ₹/hour per vehicle type.
- **Slots** — *Owner Panel → Manage Parking Slots* — set number of floors (1–26) and slots per floor.
- **Floor allotment** — *Manage Parking Slots → Allot Vehicle Types to Floors* — choose which vehicle types can park on each floor.

---

## Technology Stack

| Component | Library |
|-----------|---------|
| GUI | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) |
| Database | SQLite (built-in `sqlite3`) |
| Images | Pillow |
| Date pickers | tkcalendar |

---

## Notes

- This is an old project.
- The documentation is by AI.

---

