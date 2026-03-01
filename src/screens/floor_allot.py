"""Allot vehicle types to specific floors."""

import customtkinter
from tkinter import IntVar, StringVar

from src.screens.base import BaseScreen
from src.config import VEHICLE_TYPES, load_vehicle_options


class FloorAllotScreen(BaseScreen):
    """Assign allowed vehicle types to individual floors."""

    def __init__(self, parent, app):
        """Build and display the floor allotment screen."""
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        """Lay out floor selector, vehicle-type checkboxes, and allot button."""
        from src.screens.slots import SlotsScreen

        back = self.create_back_button(self, SlotsScreen)
        back.pack(anchor="nw", padx=10, pady=10)

        customtkinter.CTkLabel(
            self, text="Allot Vehicle Types to Floors",
            font=self.get_font(size_offset=6, weight="bold"),
        ).pack(pady=(5, 10))

        floors = self.db.get_all_floors()
        if not floors:
            customtkinter.CTkLabel(
                self,
                text="No floors configured — set up parking slots first.",
                font=self.get_font(),
            ).pack(pady=30)
            return

        floor_names = [f"Floor {i+1} ({f})" for i, f in enumerate(floors)]
        self._fmap = dict(zip(floor_names, floors))

        sel = customtkinter.CTkFrame(self, fg_color="transparent")
        sel.pack(pady=10)

        customtkinter.CTkLabel(
            sel, text="Select Floor:", font=self.get_font()
        ).grid(row=0, column=0, padx=5)
        self.floor_var = StringVar(value=floor_names[0])
        customtkinter.CTkOptionMenu(
            sel, values=floor_names, variable=self.floor_var,
            font=self.get_font(), dropdown_font=self.get_font(),
            command=self._on_floor,
        ).grid(row=0, column=1, padx=5)

        box = customtkinter.CTkFrame(self, fg_color="transparent")
        box.pack(pady=10)

        active = load_vehicle_options()
        self.cvars: dict[str, IntVar] = {}
        cols = 3

        for i, vt in enumerate(VEHICLE_TYPES):
            v = IntVar(value=0)
            self.cvars[vt] = v
            customtkinter.CTkCheckBox(
                box, text=vt, variable=v, font=self.get_font(),
                state="normal" if vt in active else "disabled",
            ).grid(row=i // cols, column=i % cols, padx=10, pady=5, sticky="w")

        customtkinter.CTkButton(
            self, text="Allot",
            font=self.get_font(weight="bold"),
            command=self._allot,
        ).pack(pady=15)

        self._on_floor(floor_names[0])

    def _on_floor(self, name: str):
        """Update checkboxes to reflect the vehicle types assigned to *name*."""
        floor = self._fmap[name]
        allotments = self.db.get_floor_vehicle_types()
        assigned = allotments.get(floor, [])
        for vt, v in self.cvars.items():
            v.set(1 if vt in assigned else 0)

    def _allot(self):
        """Save the selected vehicle types to the chosen floor."""
        floor = self._fmap[self.floor_var.get()]
        selected = [vt for vt, v in self.cvars.items() if v.get() == 1]
        try:
            self.db.set_floor_vehicle_types(floor, selected)
            self.show_info("Success",
                           f"Vehicle types updated for floor {floor}.")
        except Exception as exc:
            self.show_error("Error", str(exc))
