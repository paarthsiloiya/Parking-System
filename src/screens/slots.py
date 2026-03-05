"""Manage parking slots (floors and capacity)."""

import customtkinter
from tkinter import StringVar

from src.screens.base import BaseScreen


class SlotsScreen(BaseScreen):
    """Configure the number of floors and slots per floor."""

    def __init__(self, parent, app):
        """Build and display the slot management screen."""
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        """Lay out current/new slot configuration, action buttons, and status."""
        from src.screens.owner import OwnerMenu

        back = self.create_back_button(self, OwnerMenu)
        back.pack(anchor="nw", padx=10, pady=10)

        customtkinter.CTkLabel(
            self, text="Manage Parking Slots",
            font=self.get_font(size_offset=8, weight="bold"),
        ).pack(pady=(5, 10))

        info = self.db.get_slots_info()

        grid = customtkinter.CTkFrame(self, fg_color="transparent")
        grid.pack(pady=10)

        headers = ("", "Current", "New Value")
        for c, h in enumerate(headers):
            customtkinter.CTkLabel(
                grid, text=h,
                font=self.get_font(weight="bold"), width=140,
            ).grid(row=0, column=c, padx=10)

        customtkinter.CTkLabel(
            grid, text="Floors:", font=self.get_font()
        ).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        customtkinter.CTkLabel(
            grid, text=str(info["floors"]), font=self.get_font()
        ).grid(row=1, column=1, pady=5)
        self.floors_var = StringVar()
        floors_entry = customtkinter.CTkEntry(
            grid, textvariable=self.floors_var, width=110,
            font=self.get_font(), placeholder_text="1-26"
        )
        floors_entry.grid(row=1, column=2, pady=5)

        customtkinter.CTkLabel(
            grid, text="Slots / Floor:", font=self.get_font()
        ).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        customtkinter.CTkLabel(
            grid, text=str(info["slots_per_floor"]), font=self.get_font()
        ).grid(row=2, column=1, pady=5)
        self.slots_var = StringVar()
        slots_entry = customtkinter.CTkEntry(
            grid, textvariable=self.slots_var, width=110,
            font=self.get_font(), placeholder_text="Slots count"
        )
        slots_entry.grid(row=2, column=2, pady=5)
        
        floors_entry.bind("<Return>", lambda _: slots_entry.focus())
        slots_entry.bind("<Return>", lambda _: self._update())

        btns = customtkinter.CTkFrame(self, fg_color="transparent")
        btns.pack(pady=10)

        customtkinter.CTkButton(
            btns, text="Update Slots",
            font=self.get_font(weight="bold"),
            command=self._update,
        ).pack(pady=5, fill="x")

        customtkinter.CTkButton(
            btns, text="Allot Vehicle Types to Floors",
            font=self.get_font(),
            command=self._open_allot,
        ).pack(pady=5, fill="x")

        self._show_status()

    def refresh(self):
        """Rebuild the screen when notified of a database change (e.g. a new
        vehicle entry or exit changes slot occupancy)."""
        self.app.show_screen(SlotsScreen)

    def _show_status(self):
        """Render the slot-status visualisation (O = Open, X = Occupied)."""

        customtkinter.CTkLabel(
            self, text="Slot Status (O = Open, X = Occupied)",
            font=self.get_font(size_offset=1, weight="bold"),
        ).pack(pady=(10, 3))

        box = customtkinter.CTkScrollableFrame(self, height=140)
        box.pack(fill="x", padx=20, pady=5)

        info = self.db.get_slots_info()
        if not info["slots"]:
            customtkinter.CTkLabel(
                box, text="No slots configured.", font=self.get_font()
            ).pack()
            return

        floors: dict[str, list] = {}
        for s in info["slots"]:
            floors.setdefault(s["floor"], []).append(s)

        for floor_key in sorted(floors):
            customtkinter.CTkLabel(
                box,
                text=f"Floor {floor_key}:",
                font=self.get_font(weight="bold"),
            ).pack(anchor="w", padx=5)

            slot_text = "  ".join(
                f"[{s['slot_id']}:{'X' if s['is_occupied'] else 'O'}]"
                for s in floors[floor_key]
            )
            customtkinter.CTkLabel(
                box, text=slot_text, font=("Consolas", 11)
            ).pack(anchor="w", padx=15)

    def _update(self):
        """Validate inputs and recreate the slot layout."""
        raw_f = self.floors_var.get().strip()
        raw_s = self.slots_var.get().strip()
        if not raw_f or not raw_s:
            self.show_error("Missing Input",
                            "Enter both number of floors and slots per floor.")
            return
        try:
            nf, ns = int(raw_f), int(raw_s)
        except ValueError:
            self.show_error("Invalid", "Please enter valid numbers.")
            return
        if not (1 <= nf <= 26) or ns < 1:
            self.show_error("Out of Range",
                            "Floors: 1-26, Slots: ≥ 1.")
            return
        if not self.show_confirm(
            "Confirm", "This resets all slot data. Continue?"
        ):
            return

        try:
            self.db.setup_slots(nf, ns)
            from src.config import load_vehicle_options
            opts = load_vehicle_options()
            for i in range(nf):
                self.db.set_floor_vehicle_types(chr(65 + i), opts)
            self.show_info("Success",
                           f"Created {nf} floor(s) \u00d7 {ns} slot(s).")
            self.app.broadcast_refresh()  # notify Entry window of new slots
            self.app.show_screen(SlotsScreen)  # rebuild this screen
        except Exception as exc:
            self.show_error("Error", str(exc))

    def _open_allot(self):
        """Navigate to the floor-vehicle-type allotment screen."""
        from src.screens.floor_allot import FloorAllotScreen
        self.app.show_screen(FloorAllotScreen)
