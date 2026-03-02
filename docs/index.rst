Parking System
==============

.. image:: https://img.shields.io/badge/python-3.10%2B-blue
   :alt: Python 3.10+

.. image:: https://img.shields.io/badge/UI-CustomTkinter-green
   :alt: CustomTkinter

.. image:: https://img.shields.io/badge/DB-SQLite-lightgrey
   :alt: SQLite

A **desktop vehicle parking management system** built with Python and
`CustomTkinter <https://github.com/TomSchimansky/CustomTkinter>`_.
It opens three simultaneous, fully-synchronised windows — **Entry**,
**Exit**, and **Admin Control** — so multiple operators can work at
the same time without a server.

.. grid:: 3
   :gutter: 2

   .. grid-item-card:: 🚗 Entry Window
      :link: usage
      :link-type: doc

      Register incoming vehicles, auto-assign tokens and parking slots.

   .. grid-item-card:: 🏁 Exit Window
      :link: usage
      :link-type: doc

      Process vehicle exits and generate itemised bills instantly.

   .. grid-item-card:: 🔑 Admin Control
      :link: usage
      :link-type: doc

      Full owner panel: pricing, records, slots, credentials, and settings.

----

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   setup
   usage

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide

   architecture
   api/index

----

Key Features
------------

* **Three simultaneous windows** — Entry, Exit, and Admin Control open
  together and stay in sync in real time.
* **Auto-billing** — calculates parking fees from duration and per-hour rates.
* **Multi-floor slot management** — configurable floors, slots per floor, and
  vehicle-type allotment per floor.
* **Dynamic pricing** — owner can set ₹/hour rates per vehicle type at any
  time.
* **Owner panel** — password-protected dashboard with records, income reports,
  credential management, and more.
* **Customisable UI** — theme (Light / Dark / System), accent colour, font
  family, font size, corner radius, and border width.
* **Zero-server SQLite database** — single portable ``data/parking.db`` file.
* **First-run bootstrap** — all tables, settings, and default credentials are
  created automatically on the first launch.
