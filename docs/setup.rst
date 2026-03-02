Setup & Installation
====================

Prerequisites
-------------

* **Python 3.10 or newer** — `Download Python <https://www.python.org/downloads/>`_
* **pip** — shipped with every standard Python installer
* **Git** — to clone the repository

Step 1 — Clone the Repository
------------------------------

.. code-block:: bash

   git clone https://github.com/paarthsiloiya/Parking-System.git
   cd Parking-System

Step 2 — Create a Virtual Environment *(recommended)*
------------------------------------------------------

.. tab-set::

   .. tab-item:: Windows

      .. code-block:: bat

         python -m venv venv
         venv\Scripts\activate

   .. tab-item:: Linux / macOS

      .. code-block:: bash

         python -m venv venv
         source venv/bin/activate

Step 3 — Install Dependencies
------------------------------

.. code-block:: bash

   pip install -r requirements.txt

The ``requirements.txt`` installs:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Package
     - Purpose
   * - ``customtkinter``
     - Modern-looking tkinter widgets
   * - ``Pillow``
     - Icon loading and image manipulation
   * - ``tkcalendar``
     - Date-picker widgets in records / income screens

Step 4 — Launch the Application
---------------------------------

.. code-block:: bash

   python run.py

Three windows open simultaneously:

================  =============================================
Window            Purpose
================  =============================================
Entry             Register incoming vehicles
Exit              Process departures and generate bills
Admin Control     Owner login gate → management dashboard
================  =============================================

First-Run Bootstrap
-------------------

On the very first launch the application automatically creates the following
resources.  No manual database setup is needed.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Resource
     - Details
   * - ``data/parking.db``
     - SQLite database with all tables and default data
   * - ``data/settings.json``
     - UI preferences (theme, font, accent colour …)
   * - ``data/credentials.json``
     - Hashed owner login — default ``admin`` / ``admin123``
   * - ``data/vehicle_options.json``
     - Enabled vehicle categories (all types active by default)
   * - Parking layout
     - 2 floors × 10 slots, all types allotted to every floor
   * - Rates
     - All vehicle types start at ₹0/hour

.. warning::

   Change the default credentials immediately after the first launch.
   Navigate to **Admin Control → Login → Change Credentials**.

Recommended First-Run Steps
----------------------------

1. Open the **Admin Control** window and log in (default: ``admin`` / ``admin123``).
2. Go to **Change Credentials** and set a secure username and password.
3. Go to **Change Pricing** and configure the ₹/hour rate for each vehicle type.
4. *(Optional)* Go to **Manage Parking Slots** to set the number of floors
   and slots per floor to match your physical layout.
5. *(Optional)* Go to **Change Vehicle Options** to disable vehicle types
   that are not applicable.

Updating
--------

.. code-block:: bash

   git pull
   pip install -r requirements.txt   # in case new dependencies were added
   python run.py

The database schema is updated automatically on the next launch.

Building the Documentation Locally
------------------------------------

.. code-block:: bash

   pip install sphinx shibuya
   sphinx-build -b html docs/ docs/_build/html
   # Open docs/_build/html/index.html in your browser
