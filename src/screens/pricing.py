"""Set per-hour pricing for each vehicle type."""

import customtkinter
from tkinter import StringVar

from src.screens.base import BaseScreen
from src.config import VEHICLE_TYPES, load_vehicle_options


class PricingScreen(BaseScreen):
    """Set per-hour rates for each vehicle type."""

    def __init__(self, parent, app):
        """Build and display the pricing editor."""
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        """Lay out a table of vehicle types with current and new rate fields."""
        from src.screens.owner import OwnerMenu

        back = self.create_back_button(self, OwnerMenu)
        back.pack(anchor="nw", padx=10, pady=10)

        customtkinter.CTkLabel(
            self, text="Set Pricing (Per Hour)",
            font=self.get_font(size_offset=8, weight="bold"),
        ).pack(pady=(5, 10))

        table = customtkinter.CTkScrollableFrame(self)
        table.pack(fill="both", expand=True, padx=20, pady=5)

        for col, header in enumerate(
            ("Vehicle Type", "Current Rate (\u20B9/hr)", "New Rate (\u20B9/hr)")
        ):
            customtkinter.CTkLabel(
                table, text=header,
                font=self.get_font(weight="bold"), width=220,
            ).grid(row=0, column=col, padx=5, pady=5)

        active = load_vehicle_options()
        rates = self.db.get_all_rates()

        self.current_vars: dict[str, StringVar] = {}
        self.new_vars: dict[str, StringVar] = {}

        for row, vtype in enumerate(VEHICLE_TYPES, start=1):
            is_active = vtype in active
            rate = rates.get(vtype, 0)

            # Type label
            customtkinter.CTkLabel(
                table, text=vtype, font=self.get_font(),
                text_color=None if is_active else "gray",
            ).grid(row=row, column=0, padx=5, pady=3, sticky="w")

            # Current rate
            cur = StringVar(value=f"{rate:.0f}")
            self.current_vars[vtype] = cur
            customtkinter.CTkLabel(
                table, textvariable=cur, font=self.get_font(),
                text_color=None if is_active else "gray",
            ).grid(row=row, column=1, padx=5, pady=3)

            # New rate entry
            nv = StringVar()
            self.new_vars[vtype] = nv
            customtkinter.CTkEntry(
                table, textvariable=nv, width=140,
                font=self.get_font(), placeholder_text="Same",
                state="normal" if is_active else "disabled",
            ).grid(row=row, column=2, padx=5, pady=3)

        # Update button
        icon = self.load_icon("update-price.png")
        customtkinter.CTkButton(
            self, text="Update Prices", image=icon,
            font=self.get_font(weight="bold"),
            command=self._update,
        ).pack(pady=15)

    def _update(self):
        """Validate new rates and persist them to the database."""
        active = load_vehicle_options()
        new_rates: dict[str, float] = {}

        for vtype in VEHICLE_TYPES:
            if vtype not in active:
                new_rates[vtype] = 0
                continue

            raw = self.new_vars[vtype].get().strip()
            if raw:
                try:
                    new_rates[vtype] = float(raw)
                except ValueError:
                    self.show_error(
                        "Invalid Input",
                        f"'{raw}' is not a valid number for {vtype}.",
                    )
                    return
            else:
                new_rates[vtype] = float(self.current_vars[vtype].get())

        try:
            self.db.set_rates(new_rates)
            for vtype, rate in new_rates.items():
                self.current_vars[vtype].set(f"{rate:.0f}")
                self.new_vars[vtype].set("")
            self.show_info("Success", "Prices updated successfully.")
        except Exception as exc:
            self.show_error("Error", f"Failed to update prices:\n{exc}")
