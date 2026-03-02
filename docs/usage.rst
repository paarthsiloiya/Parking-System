Usage Guide
===========

The application opens **three separate windows** on launch.  Each window is
independent so multiple operators can work simultaneously; all windows share
one database and stay synchronised automatically — no manual refresh needed.

.. contents:: On this page
   :local:
   :depth: 2

----

Entry Window
------------

Use this window to register a vehicle that has just arrived at the parking
facility.

.. rubric:: Workflow

1. Type the **vehicle number** (e.g. ``KA01AB1234``) in the input field.
   The number is automatically converted to uppercase.
2. Select the **vehicle type** from the dropdown.
3. Click **Enter Vehicle**.

On success a pop-up shows:

* Assigned **parking slot** (e.g. ``A-03``)
* Generated 7-digit **token number** — give this to the vehicle owner

The Exit and Admin windows refresh automatically so the new entry is
visible immediately.

.. rubric:: Error cases

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Message
     - Cause
   * - *"Please enter a vehicle number."*
     - The vehicle number field is empty
   * - *"Please select a vehicle type."*
     - No type has been chosen from the dropdown
   * - *"Vehicle … is already parked inside."*
     - A record for that number already exists in the DB
   * - *"No parking slots available."*
     - All slots on floors that accept this vehicle type are occupied

----

Exit Window
-----------

Use this window to process a departing vehicle and generate a bill.

.. rubric:: Workflow

1. Type the **vehicle number** and press **Enter** or click **Generate Bill**.
2. A bill dialog appears showing:

   * Vehicle number and type
   * Assigned slot
   * Token number
   * Entry and exit timestamps
   * Parking duration
   * **Total amount due** (duration × ₹/hour rate)

3. Collect the payment and close the dialog.  The slot is freed and the
   record updated automatically.

.. tip::

   The vehicle number field accepts the **Enter** key as a shortcut for
   the Generate Bill button.

----

Admin Control Window
--------------------

The Admin Control window starts on a **login screen**.  Enter the owner
credentials to reach the management dashboard.

Default credentials: ``admin`` / ``admin123``

.. warning::

   Change these immediately after the first launch via **Change Credentials**.

Dashboard Options
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Option
     - Description
   * - **Change Credentials**
     - Update the owner username and/or password
   * - **View Records**
     - Browse parking records filtered by a date-range picker
   * - **Delete Records**
     - Remove records (all at once, by date range, or by vehicle number)
   * - **Change Vehicle Options**
     - Enable or disable specific vehicle types
   * - **View Income**
     - Calculate total income for a selected date range
   * - **Change Pricing**
     - Set the ₹/hour rate for every vehicle type
   * - **Manage Parking Slots**
     - Reconfigure number of floors, slots per floor, and floor allotments
   * - **Settings**
     - Adjust UI preferences (theme, font, accent colour, etc.)

Navigating back from any sub-screen returns to the **dashboard**.
Clicking **← Back** from the dashboard re-locks the Admin window to
the login screen.

----

Settings Screen
---------------

Access via **Admin Control → Settings**.

.. list-table::
   :header-rows: 1
   :widths: 25 15 20 40

   * - Setting
     - Type
     - Default
     - Description
   * - Font Family
     - string
     - ``Roboto``
     - Font used across all windows (any system font)
   * - Font Size
     - integer
     - ``14``
     - Base size in points; headings scale relative to this
   * - Theme
     - choice
     - ``Dark``
     - ``System``, ``Light``, or ``Dark``
   * - Accent Color
     - choice
     - ``blue``
     - ``blue``, ``green``, or ``dark-blue``
   * - Corner Radius
     - integer
     - ``12``
     - Border radius applied to buttons and inputs
   * - Border Width
     - integer
     - ``0``
     - Border thickness on buttons and inputs

.. note::

   Theme and accent-colour changes take full effect after an application
   restart.  All other settings apply immediately within each window.

----

Data Files
----------

All configuration is stored as human-readable JSON in the ``data/`` folder.

``data/settings.json``
~~~~~~~~~~~~~~~~~~~~~~~

UI preferences — edit through the **Settings** screen or directly in the
file (requires restart).

``data/credentials.json``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Contains the owner ``username`` and a SHA-256 ``password_hash``.  Always use
the **Change Credentials** screen rather than editing this file manually.

``data/vehicle_options.json``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A JSON array of currently active vehicle-type strings.  Managed through
**Change Vehicle Options**.

``data/parking.db``
~~~~~~~~~~~~~~~~~~~~

SQLite database containing:

* ``parking_records`` — every entry and exit event
* ``parking_slots`` — current slot inventory and occupancy
* ``floor_vehicle_types`` — which vehicle types may park on each floor
* ``pricing`` — per-hour rates per vehicle type

----

Keyboard Shortcuts
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Shortcut
     - Action
   * - ``Enter`` (Exit window)
     - Submit vehicle number → generate bill
   * - ``Enter`` (Owner Login, username field)
     - Move focus to password field
   * - ``Enter`` (Owner Login, password field)
     - Attempt login
