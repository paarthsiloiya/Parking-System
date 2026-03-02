"""Vehicle entry screen."""

import random

import customtkinter
from tkinter import StringVar

from src.screens.base import BaseScreen
from src.config import load_vehicle_options


class EntryScreen(BaseScreen):
    """Form for registering a new vehicle entry."""

    def __init__(self, parent, app):
        """Build and display the vehicle entry form."""
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        """Lay out the entry form — vehicle number, type, and submit button."""
        customtkinter.CTkLabel(
            self, text="Vehicle Entry",
            font=self.get_font(size_offset=8, weight="bold"),
        ).pack(pady=(10, 30))

        form = customtkinter.CTkFrame(self, fg_color="transparent")
        form.pack(pady=10)

        cr = self.settings["corner_radius"]
        bw = self.settings["border_width"]

        customtkinter.CTkLabel(
            form, text="Vehicle Number:", font=self.get_font()
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.car_no = StringVar()
        customtkinter.CTkEntry(
            form, textvariable=self.car_no, width=250,
            font=self.get_font(), corner_radius=cr, border_width=bw + 1,
        ).grid(row=0, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(
            form, text="Vehicle Type:", font=self.get_font()
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")

        options = load_vehicle_options()
        self.vehicle_type = StringVar(value="Select Vehicle Type")
        customtkinter.CTkOptionMenu(
            form, values=options, variable=self.vehicle_type,
            width=250, font=self.get_font(), dropdown_font=self.get_font(),
            corner_radius=cr,
        ).grid(row=1, column=1, padx=10, pady=10)

        icon = self.load_icon("login.png")
        customtkinter.CTkButton(
            form, text="Enter Vehicle", image=icon,
            font=self.get_font(weight="bold"),
            corner_radius=cr, border_width=bw,
            command=self._submit,
        ).grid(row=2, column=0, columnspan=2, pady=20, sticky="ew", padx=10)

    # ------------------------------------------------------------------

    @staticmethod
    def _generate_token() -> int:
        """Return a random 7-digit token number."""
        return random.randint(1_000_000, 9_999_999)

    def _submit(self):
        """Validate inputs, assign a slot, and record the vehicle entry."""
        car_no = self.car_no.get().strip().upper()
        v_type = self.vehicle_type.get()

        if not car_no:
            self.show_error("Missing Input", "Please enter a vehicle number.")
            return
        if v_type == "Select Vehicle Type":
            self.show_error("Missing Input", "Please select a vehicle type.")
            return
        if self.db.check_vehicle_inside(car_no):
            self.show_error(
                "Duplicate Entry",
                f"Vehicle {car_no} is already parked inside.",
            )
            return

        slot = self.db.get_available_slot(v_type)
        if not slot:
            self.show_error("No Slots", "No parking slots available.")
            return

        token = self._generate_token()
        try:
            self.db.entry_vehicle(car_no, v_type, token, slot)
            self.show_info(
                "Success",
                f"Vehicle {car_no} has been parked.\n"
                f"Slot: {slot}\nToken: {token}",
            )
            self.car_no.set("")
            self.vehicle_type.set("Select Vehicle Type")
            # Notify the Exit and Admin windows so they see the new record
            # immediately without the operator having to refresh manually.
            self.app.broadcast_refresh()
        except Exception as exc:
            self.show_error("Error", f"Failed to register vehicle:\n{exc}")
