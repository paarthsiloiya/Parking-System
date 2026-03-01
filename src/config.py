"""Configuration management for the Parking System.

Handles settings, credentials, vehicle options, and path constants.
All config files are stored as JSON in the data/ directory.
"""

import json
import hashlib
import os

# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
DB_PATH = os.path.join(DATA_DIR, "parking.db")

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DEFAULT_SETTINGS = {
    "font_family": "Roboto",
    "font_size": 14,
    "theme": "Dark",
    "accent_color": "blue",
    "corner_radius": 12,
    "border_width": 0,
}

DEFAULT_CREDENTIALS = {
    "username": "admin",
    "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
}

VEHICLE_TYPES = [
    "Two Wheeler",
    "Three Wheeler (Passenger)",
    "Three Wheeler (Freight)",
    "Four Wheeler (Passenger)",
    "Four Wheeler (Freight)",
    "Mini Bus",
    "Bus",
    "Mini Truck",
    "Truck",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_data_dir():
    """Create the data directory if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _read_json(filename, defaults):
    """Read a JSON config file, creating it with *defaults* if missing."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        _write_json(filename, defaults)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _write_json(filename, data):
    """Write *data* to a JSON config file."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

def load_settings() -> dict:
    """Load UI settings from ``settings.json``.

    :returns: Settings dictionary with keys such as ``font_family``,
        ``font_size``, ``theme``, ``accent_color``, ``corner_radius``,
        and ``border_width``.
    """
    return _read_json("settings.json", DEFAULT_SETTINGS)


def save_settings(settings: dict):
    """Persist UI settings to ``settings.json``.

    :param settings: Complete settings dictionary to write.
    """
    _write_json("settings.json", settings)


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------

def load_credentials() -> dict:
    """Load owner credentials from ``credentials.json``.

    :returns: Dictionary with ``username`` and ``password_hash`` keys.
    """
    return _read_json("credentials.json", DEFAULT_CREDENTIALS)


def save_credentials(creds: dict):
    """Persist owner credentials to ``credentials.json``.

    :param creds: Dictionary with ``username`` and ``password_hash``.
    """
    _write_json("credentials.json", creds)


def hash_password(password: str) -> str:
    """Return the SHA-256 hex digest of *password*.

    :param password: Plain-text password.
    :returns: Hex-encoded hash string.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Check whether *password* matches the stored hash.

    :param password: Plain-text password to verify.
    :param password_hash: Expected SHA-256 hex digest.
    :returns: ``True`` if the password is correct.
    """
    return hash_password(password) == password_hash


# ---------------------------------------------------------------------------
# Vehicle options
# ---------------------------------------------------------------------------

def load_vehicle_options() -> list:
    """Load the list of enabled vehicle type names.

    :returns: List of vehicle type strings currently active.
    """
    return _read_json("vehicle_options.json", VEHICLE_TYPES[:])


def save_vehicle_options(options: list):
    """Persist the list of enabled vehicle types.

    :param options: List of vehicle type strings to save.
    """
    _write_json("vehicle_options.json", options)
