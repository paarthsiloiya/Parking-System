Architecture
============

.. contents:: On this page
   :local:
   :depth: 2

----

Overview
--------

The application is a **single-process, multi-window desktop application**
built on Python's ``tkinter`` toolkit via the ``CustomTkinter`` wrapper.
A single SQLite database file is shared by all three windows through one
``Database`` instance held by the central coordinator.

.. code-block:: text

   run.py
     └── ParkingApp  (coordinator — owns db, settings)
           ├── ParkingWindow  "Entry — Parking System"
           │     └── EntryScreen
           ├── ParkingWindow  "Exit — Parking System"
           │     └── ExitScreen
           └── ParkingWindow  "Admin Control — Parking System"
                 └── OwnerLogin → OwnerMenu → [admin screens …]

----

Module Map
----------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Module
     - Responsibility
   * - ``src/app.py``
     - :class:`~src.app.ParkingApp` coordinator and
       :class:`~src.app.ParkingWindow` top-level window wrapper
   * - ``src/database.py``
     - All SQLite queries via :class:`~src.database.Database`
   * - ``src/config.py``
     - Path constants, JSON config helpers, credential utilities
   * - ``src/screens/base.py``
     - :class:`~src.screens.base.BaseScreen` — shared helpers for every screen
   * - ``src/screens/entry.py``
     - Vehicle entry form
   * - ``src/screens/exit_screen.py``
     - Vehicle exit form and bill trigger
   * - ``src/screens/bill.py``
     - Bill dialog (modal ``CTkToplevel``)
   * - ``src/screens/owner.py``
     - ``OwnerLogin`` gate and ``OwnerMenu`` dashboard
   * - ``src/screens/credentials.py``
     - Change username / password
   * - ``src/screens/records.py``
     - Browse parking records by date range
   * - ``src/screens/delete_records.py``
     - Delete records (all / by date / by vehicle)
   * - ``src/screens/income.py``
     - Income calculator
   * - ``src/screens/pricing.py``
     - Per-vehicle-type hourly rate editor
   * - ``src/screens/slots.py``
     - Floor and slot count configuration
   * - ``src/screens/floor_allot.py``
     - Per-floor vehicle-type allotment
   * - ``src/screens/vehicle_options.py``
     - Enable / disable vehicle categories
   * - ``src/screens/settings_screen.py``
     - UI preference editor

----

Multi-Window Coordination
--------------------------

``ParkingApp``
~~~~~~~~~~~~~~

A plain Python class (not a ``CTk`` widget) that acts as the shared-state
hub.  It owns:

* A hidden ``CTk`` root window that drives the tkinter event loop.
* A single :class:`~src.database.Database` instance shared by all windows.
* The current ``settings`` dictionary.
* The list of all open :class:`~src.app.ParkingWindow` instances.
* The ``broadcast_refresh()`` method.

``ParkingWindow``
~~~~~~~~~~~~~~~~~

A ``CTkToplevel`` subclass.  Each of the three user-facing windows is an
independent ``ParkingWindow``.  It:

* Maintains its own current screen via ``show_screen()``.
* Proxies ``db``, ``settings``, ``get_font()``, ``reload_settings()``, and
  ``broadcast_refresh()`` to the coordinator so every screen can call
  ``self.app.*`` without knowing whether ``app`` is the coordinator or a
  window.
* Implements ``_refresh_current()`` which calls ``screen.refresh()`` if the
  currently displayed screen supports it.

Live Sync Flow
~~~~~~~~~~~~~~

.. code-block:: text

   Operator parks a vehicle (EntryScreen._submit)
       │
       ▼
   db.entry_vehicle(…)           ← SQLite write
       │
       ▼
   self.app.broadcast_refresh()  ← ParkingWindow.broadcast_refresh()
       │                            delegates to ParkingApp.broadcast_refresh()
       ▼
   For every ParkingWindow:
       window._refresh_current() ← calls screen.refresh() if present

Screens that implement ``refresh()``:

* :class:`~src.screens.records.RecordsScreen` — re-fetches the record list
* :class:`~src.screens.income.IncomeScreen` — recalculates income
* :class:`~src.screens.slots.SlotsScreen` — rebuilds slot-status visualisation

----

Screen Lifecycle
----------------

Each screen is a ``CTkFrame`` subclass that inherits
:class:`~src.screens.base.BaseScreen`.  When ``show_screen(ScreenClass)`` is
called on a window:

1. The current frame is ``destroy()``-ed.
2. A new instance of ``ScreenClass`` is created with ``(container, window)``
   as arguments.
3. It is ``pack()``-ed to fill the window container.

This means **screens are stateless between navigations** — all widget
variables are re-created fresh on each display.

----

Database Layer
--------------

:class:`~src.database.Database` uses a context-manager helper ``_connect()``
that:

* Opens a **new connection per operation** (safe for single-process use with
  SQLite WAL mode).
* Enables ``PRAGMA foreign_keys = ON`` and ``PRAGMA journal_mode = WAL``.
* Commits on success, rolls back on any exception, and always closes.

Key tables:

.. list-table::
   :header-rows: 1

   * - Table
     - Primary key
     - Notes
   * - ``parking_records``
     - ``id`` (autoincrement)
     - One row per vehicle entry; ``time_of_exit`` and ``bill_paid`` NULL until exit
   * - ``parking_slots``
     - ``slot_name`` (e.g. ``A-01``)
     - ``is_occupied`` flag updated atomically with the record
   * - ``floor_vehicle_types``
     - ``(floor, vehicle_type)``
     - Controls which types may enter each floor
   * - ``pricing``
     - ``vehicle_type``
     - ₹/hour rate

----

Configuration Files
-------------------

All JSON config files are stored in ``data/`` and loaded on demand (not
cached at module level) so settings changes are picked up without restart
where possible.

.. list-table::
   :header-rows: 1

   * - File
     - Loaded by
     - Written by
   * - ``data/settings.json``
     - :func:`~src.config.load_settings`
     - :func:`~src.config.save_settings`
   * - ``data/credentials.json``
     - :func:`~src.config.load_credentials`
     - :func:`~src.config.save_credentials`
   * - ``data/vehicle_options.json``
     - :func:`~src.config.load_vehicle_options`
     - :func:`~src.config.save_vehicle_options`
