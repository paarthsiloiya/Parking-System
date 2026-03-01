"""SQLite database handler for the Parking System.

Replaces the original MySQL + pickle approach with a single portable
SQLite database.  All queries use parameterised placeholders to prevent
SQL injection.
"""

import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime
from math import ceil

from src.config import DB_PATH, DATA_DIR, VEHICLE_TYPES, load_vehicle_options


class Database:
    """Manages all parking system data in an SQLite database."""

    def __init__(self):
        """Initialise the database, creating the schema if needed."""
        os.makedirs(DATA_DIR, exist_ok=True)
        self.db_path = DB_PATH
        self._init_db()
        self._first_run_setup()

    # ------------------------------------------------------------------
    # Connection helper
    # ------------------------------------------------------------------

    @contextmanager
    def _connect(self):
        """Yield an SQLite connection with WAL mode and foreign keys enabled.

        Commits on success, rolls back on exception, and closes the
        connection when done.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _init_db(self):
        """Create database tables and indexes if they do not exist."""
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS parking_records (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    car_no        TEXT    NOT NULL,
                    vehicle_type  TEXT    NOT NULL,
                    token_number  INTEGER NOT NULL UNIQUE,
                    bill_paid     REAL,
                    time_of_entry TEXT    NOT NULL,
                    time_of_exit  TEXT,
                    slot          TEXT    NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS parking_slots (
                    slot_id     TEXT PRIMARY KEY,
                    floor       TEXT    NOT NULL,
                    is_occupied INTEGER DEFAULT 0
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS floor_vehicle_types (
                    floor        TEXT NOT NULL,
                    vehicle_type TEXT NOT NULL,
                    PRIMARY KEY (floor, vehicle_type)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vehicle_rates (
                    vehicle_type  TEXT PRIMARY KEY,
                    rate_per_hour REAL DEFAULT 0
                )
            """)
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_car_no "
                "ON parking_records(car_no)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_entry_time "
                "ON parking_records(time_of_entry)"
            )

    def _first_run_setup(self):
        """Populate default data when the database is brand-new."""
        info = self.get_slots_info()
        if info["floors"] > 0:
            return  # already initialised

        # Default: 2 floors, 10 slots each
        self.setup_slots(2, 10)

        # Default rates (all zero)
        for vt in VEHICLE_TYPES:
            self.set_rate(vt, 0)

        # All active vehicle types assigned to every floor
        options = load_vehicle_options()
        for floor_letter in ("A", "B"):
            self.set_floor_vehicle_types(floor_letter, options)

    # ------------------------------------------------------------------
    # Vehicle entry / exit
    # ------------------------------------------------------------------

    def entry_vehicle(self, car_no: str, vehicle_type: str,
                      token_number: int, slot: str):
        """Register a vehicle entry and mark its slot as occupied.

        :param car_no: Vehicle registration number.
        :param vehicle_type: Category of the vehicle.
        :param token_number: Unique token issued to the driver.
        :param slot: Slot identifier (e.g. ``'A1'``).
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO parking_records
                       (car_no, vehicle_type, token_number, time_of_entry, slot)
                   VALUES (?, ?, ?, ?, ?)""",
                (car_no, vehicle_type, token_number,
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"), slot),
            )
            cur.execute(
                "UPDATE parking_slots SET is_occupied = 1 WHERE slot_id = ?",
                (slot,),
            )

    def exit_vehicle(self, car_no: str) -> dict | None:
        """Process vehicle exit — returns bill data dict or None."""
        with self._connect() as conn:
            cur = conn.cursor()
            exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cur.execute(
                """SELECT id, vehicle_type, token_number, time_of_entry, slot
                   FROM parking_records
                   WHERE car_no = ? AND time_of_exit IS NULL""",
                (car_no,),
            )
            row = cur.fetchone()
            if not row:
                return None

            record_id = row["id"]
            vehicle_type = row["vehicle_type"]
            token_number = row["token_number"]
            entry_time_str = row["time_of_entry"]
            slot = row["slot"]

            # Calculate bill
            entry_dt = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
            exit_dt = datetime.strptime(exit_time, "%Y-%m-%d %H:%M:%S")
            diff_seconds = (exit_dt - entry_dt).total_seconds()
            hours = max(1, ceil(diff_seconds / 3600))
            rate = self.get_rate(vehicle_type)
            bill = rate * hours

            # Update record
            cur.execute(
                """UPDATE parking_records
                   SET time_of_exit = ?, bill_paid = ?
                   WHERE id = ?""",
                (exit_time, bill, record_id),
            )

            # Free the slot
            cur.execute(
                "UPDATE parking_slots SET is_occupied = 0 WHERE slot_id = ?",
                (slot,),
            )

            return {
                "car_no": car_no,
                "vehicle_type": vehicle_type,
                "token_number": token_number,
                "entry_time": entry_time_str,
                "exit_time": exit_time,
                "slot": slot,
                "bill": bill,
            }

    def check_vehicle_inside(self, car_no: str) -> bool:
        """Return ``True`` if *car_no* is currently parked (no exit recorded).

        :param car_no: Vehicle registration number.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT 1 FROM parking_records
                   WHERE car_no = ? AND time_of_exit IS NULL""",
                (car_no,),
            )
            return cur.fetchone() is not None

    # ------------------------------------------------------------------
    # Records
    # ------------------------------------------------------------------

    def get_records(self, from_date: str, to_date: str) -> list[dict]:
        """Fetch parking records whose entry time falls in a date range.

        :param from_date: Start datetime string (``YYYY-MM-DD HH:MM:SS``).
        :param to_date: End datetime string (``YYYY-MM-DD HH:MM:SS``).
        :returns: List of record dictionaries.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT * FROM parking_records
                   WHERE time_of_entry BETWEEN ? AND ?
                   ORDER BY time_of_entry""",
                (from_date, to_date),
            )
            return [dict(r) for r in cur.fetchall()]

    def get_income(self, from_date: str, to_date: str) -> float:
        """Return total income from paid bills in a date range.

        :param from_date: Start datetime string.
        :param to_date: End datetime string.
        :returns: Sum of ``bill_paid`` values.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT COALESCE(SUM(bill_paid), 0) AS total
                   FROM parking_records
                   WHERE time_of_entry BETWEEN ? AND ?
                     AND bill_paid IS NOT NULL""",
                (from_date, to_date),
            )
            row = cur.fetchone()
            return float(row["total"]) if row else 0.0

    def delete_all_records(self):
        """Delete every row from the parking records table."""
        with self._connect() as conn:
            conn.cursor().execute("DELETE FROM parking_records")

    def delete_records_by_date(self, from_date: str, to_date: str):
        """Delete parking records whose entry time falls in a date range.

        :param from_date: Start datetime string.
        :param to_date: End datetime string.
        """
        with self._connect() as conn:
            conn.cursor().execute(
                "DELETE FROM parking_records "
                "WHERE time_of_entry BETWEEN ? AND ?",
                (from_date, to_date),
            )

    def delete_records_by_car(self, car_no: str):
        """Delete all parking records for a specific vehicle.

        :param car_no: Vehicle registration number.
        """
        with self._connect() as conn:
            conn.cursor().execute(
                "DELETE FROM parking_records WHERE car_no = ?",
                (car_no,),
            )

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def get_available_slot(self, vehicle_type: str) -> str | None:
        """Find the first free slot suitable for *vehicle_type*.

        Prefers floors that are assigned this vehicle type. Falls back
        to any free slot if no matching floor has vacancies.

        :param vehicle_type: Category of the vehicle.
        :returns: Slot identifier string, or ``None`` if full.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            # Prefer a floor that's assigned this vehicle type
            cur.execute(
                """SELECT ps.slot_id
                   FROM parking_slots ps
                   JOIN floor_vehicle_types fvt ON ps.floor = fvt.floor
                   WHERE fvt.vehicle_type = ? AND ps.is_occupied = 0
                   ORDER BY ps.slot_id
                   LIMIT 1""",
                (vehicle_type,),
            )
            row = cur.fetchone()
            if row:
                return row["slot_id"]

            # Fallback: any free slot
            cur.execute(
                "SELECT slot_id FROM parking_slots "
                "WHERE is_occupied = 0 ORDER BY slot_id LIMIT 1"
            )
            row = cur.fetchone()
            return row["slot_id"] if row else None

    def setup_slots(self, num_floors: int, slots_per_floor: int):
        """Recreate the parking slot layout.

        Deletes all existing slots and floor-vehicle-type mappings,
        then creates *num_floors* floors (A, B, …) each with
        *slots_per_floor* slots.

        :param num_floors: Number of floors (1–26).
        :param slots_per_floor: Number of slots on each floor.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM parking_slots")
            cur.execute("DELETE FROM floor_vehicle_types")
            for f in range(num_floors):
                floor = chr(65 + f)
                for s in range(1, slots_per_floor + 1):
                    slot_id = f"{floor}{s}"
                    cur.execute(
                        "INSERT INTO parking_slots "
                        "(slot_id, floor, is_occupied) VALUES (?, ?, 0)",
                        (slot_id, floor),
                    )

    def get_slots_info(self) -> dict:
        """Return a summary of all parking slots.

        :returns: Dictionary with ``floors`` count, ``slots_per_floor``
            count, and a ``slots`` list of slot dictionaries.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM parking_slots ORDER BY slot_id")
            rows = [dict(r) for r in cur.fetchall()]
            if not rows:
                return {"floors": 0, "slots_per_floor": 0, "slots": []}

            floors = sorted({r["floor"] for r in rows})
            first_floor_slots = [r for r in rows if r["floor"] == floors[0]]
            return {
                "floors": len(floors),
                "slots_per_floor": len(first_floor_slots),
                "slots": rows,
            }

    # ------------------------------------------------------------------
    # Floor ↔ vehicle-type mapping
    # ------------------------------------------------------------------

    def set_floor_vehicle_types(self, floor: str, vehicle_types: list[str]):
        """Replace the allowed vehicle types for a floor.

        :param floor: Single-letter floor identifier (e.g. ``'A'``).
        :param vehicle_types: List of vehicle type strings to assign.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM floor_vehicle_types WHERE floor = ?", (floor,)
            )
            for vt in vehicle_types:
                cur.execute(
                    "INSERT INTO floor_vehicle_types (floor, vehicle_type) "
                    "VALUES (?, ?)",
                    (floor, vt),
                )

    def get_floor_vehicle_types(self) -> dict[str, list[str]]:
        """Return a mapping of floor letters to their allowed vehicle types.

        :returns: ``{floor: [vehicle_type, …], …}`` dictionary.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM floor_vehicle_types ORDER BY floor"
            )
            result: dict[str, list[str]] = {}
            for row in cur.fetchall():
                result.setdefault(row["floor"], []).append(row["vehicle_type"])
            return result

    def get_all_floors(self) -> list[str]:
        """Return a sorted list of all floor letters.

        :returns: e.g. ``['A', 'B']``.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT DISTINCT floor FROM parking_slots ORDER BY floor"
            )
            return [row["floor"] for row in cur.fetchall()]

    # ------------------------------------------------------------------
    # Rates
    # ------------------------------------------------------------------

    def get_rate(self, vehicle_type: str) -> float:
        """Return the per-hour rate for a vehicle type.

        :param vehicle_type: Vehicle category name.
        :returns: Rate in currency units, or ``0.0`` if not set.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT rate_per_hour FROM vehicle_rates "
                "WHERE vehicle_type = ?",
                (vehicle_type,),
            )
            row = cur.fetchone()
            return float(row["rate_per_hour"]) if row else 0.0

    def get_all_rates(self) -> dict[str, float]:
        """Return all vehicle-type rates.

        :returns: ``{vehicle_type: rate_per_hour, …}`` dictionary.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM vehicle_rates ORDER BY vehicle_type")
            return {
                row["vehicle_type"]: float(row["rate_per_hour"])
                for row in cur.fetchall()
            }

    def set_rate(self, vehicle_type: str, rate: float):
        """Set the per-hour rate for a single vehicle type.

        Inserts or updates the row using ``ON CONFLICT``.

        :param vehicle_type: Vehicle category name.
        :param rate: New per-hour rate.
        """
        with self._connect() as conn:
            conn.cursor().execute(
                """INSERT INTO vehicle_rates (vehicle_type, rate_per_hour)
                   VALUES (?, ?)
                   ON CONFLICT(vehicle_type)
                   DO UPDATE SET rate_per_hour = excluded.rate_per_hour""",
                (vehicle_type, rate),
            )

    def set_rates(self, rates: dict[str, float]):
        """Set per-hour rates for multiple vehicle types at once.

        :param rates: ``{vehicle_type: rate_per_hour, …}`` dictionary.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            for vt, rate in rates.items():
                cur.execute(
                    """INSERT INTO vehicle_rates (vehicle_type, rate_per_hour)
                       VALUES (?, ?)
                       ON CONFLICT(vehicle_type)
                       DO UPDATE SET rate_per_hour = excluded.rate_per_hour""",
                    (vt, rate),
                )
