"""View parking records screen."""

import customtkinter
from tkcalendar import DateEntry

from src.screens.base import BaseScreen


class RecordsScreen(BaseScreen):
    """Browse parking records by date range."""

    def __init__(self, parent, app):
        """Build and display the records viewer."""
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        """Lay out date pickers, fetch button, and records text area."""
        from src.screens.owner import OwnerMenu

        back = self.create_back_button(self, OwnerMenu)
        back.pack(anchor="nw", padx=10, pady=10)

        customtkinter.CTkLabel(
            self, text="View Records",
            font=self.get_font(size_offset=8, weight="bold"),
        ).pack(pady=(5, 10))

        picker_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        picker_frame.pack(pady=5)

        customtkinter.CTkLabel(
            picker_frame, text="From:", font=self.get_font()
        ).grid(row=0, column=0, padx=5, pady=5)
        self.from_cal = DateEntry(
            picker_frame, width=15, date_pattern="yyyy-mm-dd"
        )
        self.from_cal.grid(row=0, column=1, padx=5, pady=5)

        customtkinter.CTkLabel(
            picker_frame, text="To:", font=self.get_font()
        ).grid(row=0, column=2, padx=(15, 5), pady=5)
        self.to_cal = DateEntry(
            picker_frame, width=15, date_pattern="yyyy-mm-dd"
        )
        self.to_cal.grid(row=0, column=3, padx=5, pady=5)

        icon = self.load_icon("GetRecord.png")
        customtkinter.CTkButton(
            picker_frame, text="Get Records", image=icon,
            font=self.get_font(), command=self._fetch,
        ).grid(row=0, column=4, padx=10, pady=5)

        self.text = customtkinter.CTkTextbox(
            self, font=("Consolas", 11), wrap="none",
        )
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh(self):
        """Re-fetch records when notified of a database change."""
        self._fetch()

    def _fetch(self):
        """Query records for the selected date range and display them."""
        from_date = self.from_cal.get_date().strftime("%Y-%m-%d 00:00:00")
        to_date = self.to_cal.get_date().strftime("%Y-%m-%d 23:59:59")

        if from_date > to_date:
            self.show_error("Invalid Range", "From date must be before To date.")
            return

        try:
            records = self.db.get_records(from_date, to_date)
            self.text.delete("1.0", "end")

            if not records:
                self.text.insert("end", "No records found for the selected period.")
                return

            hdr = (
                f"{'Vehicle No':<15}"
                f"{'Type':<28}"
                f"{'Token':<10}"
                f"{'Bill':<10}"
                f"{'Entry Time':<20}"
                f"{'Exit Time':<20}"
                f"{'Slot':<6}"
            )
            self.text.insert("end", hdr + "\n")
            self.text.insert("end", "-" * len(hdr) + "\n")

            for r in records:
                exit_t = r.get("time_of_exit") or "Still Parked"
                bill = f"\u20B9{r.get('bill_paid') or 0:.0f}"
                line = (
                    f"{r['car_no']:<15}"
                    f"{r['vehicle_type']:<28}"
                    f"{r['token_number']:<10}"
                    f"{bill:<10}"
                    f"{r['time_of_entry']:<20}"
                    f"{exit_t:<20}"
                    f"{r['slot']:<6}"
                )
                self.text.insert("end", line + "\n")

            self.text.insert("end", f"\nTotal records: {len(records)}")

        except Exception as exc:
            self.show_error("Error", f"Failed to fetch records:\n{exc}")
