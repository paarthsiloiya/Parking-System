"""Parking System - Entry Point.

Launch the parking management application.
"""

import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import ParkingApp


def main():
    app = ParkingApp()
    app.mainloop()


if __name__ == "__main__":
    main()
