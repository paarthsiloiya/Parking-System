"""View income screen."""

import customtkinter
from tkcalendar import DateEntry

from src.screens.base import BaseScreen


class IncomeScreen(BaseScreen):
    """View total parking income for a date range."""

    def __init__(self, parent, app):
        """Build and display the income viewer."""
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        """Lay out date pickers, calculate button, and amount label."""
        from src.screens.owner import OwnerMenu

        back = self.create_back_button(self, OwnerMenu)
        back.pack(anchor="nw", padx=10, pady=10)

        customtkinter.CTkLabel(
            self, text="View Income",
            font=self.get_font(size_offset=8, weight="bold"),
        ).pack(pady=(10, 20))

        picker = customtkinter.CTkFrame(self, fg_color="transparent")
        picker.pack(pady=10)

        customtkinter.CTkLabel(
            picker, text="From:", font=self.get_font()
        ).grid(row=0, column=0, padx=5, pady=5)
        self.from_cal = DateEntry(
            picker, width=15, date_pattern="yyyy-mm-dd"
        )
        self.from_cal.grid(row=0, column=1, padx=5, pady=5)

        customtkinter.CTkLabel(
            picker, text="To:", font=self.get_font()
        ).grid(row=0, column=2, padx=(15, 5), pady=5)
        self.to_cal = DateEntry(
            picker, width=15, date_pattern="yyyy-mm-dd"
        )
        self.to_cal.grid(row=0, column=3, padx=5, pady=5)

        icon = self.load_icon("GetIncome.png")
        customtkinter.CTkButton(
            self, text="Calculate Income", image=icon,
            font=self.get_font(weight="bold"),
            command=self._calculate,
        ).pack(pady=15)

        self.amount_label = customtkinter.CTkLabel(
            self, text="",
            font=self.get_font(size_offset=16, weight="bold"),
        )
        self.amount_label.pack(pady=30)

    def refresh(self):
        """Recalculate income when notified of a database change."""
        self._calculate()

    def _calculate(self):
        """Query income for the selected date range and display it."""
        from_date = self.from_cal.get_date().strftime("%Y-%m-%d 00:00:00")
        to_date = self.to_cal.get_date().strftime("%Y-%m-%d 23:59:59")

        if from_date > to_date:
            self.show_error("Invalid Range", "From date must be before To date.")
            return

        try:
            income = self.db.get_income(from_date, to_date)
            self.amount_label.configure(text=f"\u20B9{income:,.2f}")
        except Exception as exc:
            self.show_error("Error", f"Failed to calculate income:\n{exc}")
