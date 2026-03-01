"""Configure which vehicle types are available."""

import customtkinter
from tkinter import IntVar

from src.screens.base import BaseScreen
from src.config import VEHICLE_TYPES, load_vehicle_options, save_vehicle_options


class VehicleOptionsScreen(BaseScreen):
    """Enable or disable vehicle types via checkboxes."""

    def __init__(self, parent, app):
        """Build and display the vehicle options editor."""
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        """Lay out checkboxes for each vehicle type and an update button."""
        from src.screens.owner import OwnerMenu

        back = self.create_back_button(self, OwnerMenu)
        back.pack(anchor="nw", padx=10, pady=10)

        customtkinter.CTkLabel(
            self, text="Vehicle Options",
            font=self.get_font(size_offset=8, weight="bold"),
        ).pack(pady=(5, 10))

        customtkinter.CTkLabel(
            self,
            text="Select which vehicle types are available for parking:",
            font=self.get_font(size_offset=-1), text_color="gray",
        ).pack(pady=5)

        grid = customtkinter.CTkFrame(self, fg_color="transparent")
        grid.pack(pady=15)

        current = load_vehicle_options()
        self.vars: dict[str, IntVar] = {}
        cols = 3

        for i, vtype in enumerate(VEHICLE_TYPES):
            var = IntVar(value=1 if vtype in current else 0)
            self.vars[vtype] = var
            customtkinter.CTkCheckBox(
                grid, text=vtype, variable=var,
                font=self.get_font(),
                corner_radius=self.settings["corner_radius"],
            ).grid(row=i // cols, column=i % cols, padx=12, pady=6, sticky="w")

        icon = self.load_icon("update-option-menue.png")
        customtkinter.CTkButton(
            self, text="Update Options", image=icon,
            font=self.get_font(weight="bold"),
            corner_radius=self.settings["corner_radius"],
            command=self._update,
        ).pack(pady=20)

    def _update(self):
        """Save the selected vehicle types to configuration."""
        selected = [vt for vt, v in self.vars.items() if v.get() == 1]
        if not selected:
            self.show_error("Error", "Select at least one vehicle type.")
            return
        save_vehicle_options(selected)
        self.show_info("Success", "Vehicle options updated.")
