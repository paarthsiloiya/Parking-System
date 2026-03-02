"""Vehicle exit screen."""

import customtkinter
from tkinter import StringVar

from src.screens.base import BaseScreen


class ExitScreen(BaseScreen):
    """Form for processing a vehicle exit and generating a bill."""

    def __init__(self, parent, app):
        """Build and display the vehicle exit form."""
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        """Lay out the exit form — vehicle number input and submit button."""
        customtkinter.CTkLabel(
            self, text="Vehicle Exit",
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
        entry = customtkinter.CTkEntry(
            form, textvariable=self.car_no, width=250,
            font=self.get_font(), corner_radius=cr, border_width=bw + 1,
        )
        entry.grid(row=0, column=1, padx=10, pady=10)
        entry.bind("<Return>", lambda _: self._submit())

        icon = self.load_icon("exit.png")
        customtkinter.CTkButton(
            form, text="Generate Bill", image=icon,
            font=self.get_font(weight="bold"),
            corner_radius=cr, border_width=bw,
            command=self._submit,
        ).grid(row=1, column=0, columnspan=2, pady=20, sticky="ew", padx=10)

    def _submit(self):
        """Validate the vehicle number, process exit, and show the bill."""
        car_no = self.car_no.get().strip().upper()

        if not car_no:
            self.show_error("Missing Input", "Please enter a vehicle number.")
            return
        if not self.db.check_vehicle_inside(car_no):
            self.show_error(
                "Not Found",
                f"No parked vehicle found with number {car_no}.",
            )
            return

        try:
            bill_data = self.db.exit_vehicle(car_no)
            if bill_data:
                from src.screens.bill import BillDialog
                BillDialog(self, bill_data, self.app)
                self.car_no.set("")
                # Notify Entry and Admin windows so the freed slot is visible
                # immediately.
                self.app.broadcast_refresh()
            else:
                self.show_error("Error", "Failed to process vehicle exit.")
        except Exception as exc:
            self.show_error("Error", f"Failed to process exit:\n{exc}")
