"""Delete parking records screen."""

import customtkinter
from tkinter import StringVar
from tkcalendar import DateEntry

from src.screens.base import BaseScreen


class DeleteRecordsScreen(BaseScreen):
    """Options for deleting parking records."""

    def __init__(self, parent, app):
        """Build and display the delete-records interface."""
        super().__init__(parent, app)
        self._frames: dict[str, customtkinter.CTkFrame] = {}
        self._create_widgets()

    def _create_widgets(self):
        """Lay out the option selector and sub-frames for each mode."""
        from src.screens.owner import OwnerMenu

        back = self.create_back_button(self, OwnerMenu)
        back.pack(anchor="nw", padx=10, pady=10)

        customtkinter.CTkLabel(
            self, text="Delete Records",
            font=self.get_font(size_offset=8, weight="bold"),
        ).pack(pady=(5, 15))

        # Option selector
        options = [
            "Select an option",
            "Delete All Records",
            "Delete by Date Range",
            "Delete by Vehicle Number",
        ]
        customtkinter.CTkOptionMenu(
            self, values=options,
            font=self.get_font(), dropdown_font=self.get_font(),
            command=self._show_option,
        ).pack(pady=10)

        self.container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

        self._build_delete_all()
        self._build_date_range()
        self._build_vehicle()

    def _build_delete_all(self):
        """Create the 'Delete All Records' sub-frame."""
        frame = customtkinter.CTkFrame(self.container, fg_color="transparent")
        icon = self.load_icon("deleteAll.png")
        customtkinter.CTkButton(
            frame, text="Delete All Records", image=icon,
            font=self.get_font(weight="bold"),
            fg_color="#c0392b", hover_color="#922b21",
            command=self._delete_all,
        ).pack(pady=20)
        customtkinter.CTkLabel(
            frame,
            text="⚠  This will permanently delete ALL parking records.",
            font=self.get_font(size_offset=-1), text_color="orange",
        ).pack()
        self._frames["Delete All Records"] = frame

    def _build_date_range(self):
        """Create the 'Delete by Date Range' sub-frame."""
        frame = customtkinter.CTkFrame(self.container, fg_color="transparent")
        inner = customtkinter.CTkFrame(frame, fg_color="transparent")
        inner.pack(pady=10)

        customtkinter.CTkLabel(inner, text="From:", font=self.get_font()).grid(
            row=0, column=0, padx=5, pady=5)
        self.del_from = DateEntry(inner, width=15, date_pattern="yyyy-mm-dd")
        self.del_from.grid(row=0, column=1, padx=5, pady=5)

        customtkinter.CTkLabel(inner, text="To:", font=self.get_font()).grid(
            row=1, column=0, padx=5, pady=5)
        self.del_to = DateEntry(inner, width=15, date_pattern="yyyy-mm-dd")
        self.del_to.grid(row=1, column=1, padx=5, pady=5)

        icon = self.load_icon("deleteAll.png")
        customtkinter.CTkButton(
            frame, text="Delete", image=icon,
            font=self.get_font(),
            fg_color="#c0392b", hover_color="#922b21",
            command=self._delete_by_date,
        ).pack(pady=10)
        self._frames["Delete by Date Range"] = frame

    def _build_vehicle(self):
        """Create the 'Delete by Vehicle Number' sub-frame."""
        frame = customtkinter.CTkFrame(self.container, fg_color="transparent")
        inner = customtkinter.CTkFrame(frame, fg_color="transparent")
        inner.pack(pady=10)

        customtkinter.CTkLabel(
            inner, text="Vehicle Number:", font=self.get_font()
        ).grid(row=0, column=0, padx=5, pady=5)
        self.del_car = StringVar()
        self.del_car_entry = customtkinter.CTkEntry(
            inner, textvariable=self.del_car, width=200,
            font=self.get_font(), placeholder_text="e.g. MH04AB1234"
        )
        self.del_car_entry.grid(row=0, column=1, padx=5, pady=5)
        self.del_car_entry.bind("<Return>", lambda _: self._delete_by_vehicle())

        icon = self.load_icon("deleteAll.png")
        customtkinter.CTkButton(
            frame, text="Delete", image=icon,
            font=self.get_font(),
            fg_color="#c0392b", hover_color="#922b21",
            command=self._delete_by_vehicle,
        ).pack(pady=10)
        self._frames["Delete by Vehicle Number"] = frame

    def _show_option(self, value: str):
        """Show the sub-frame matching *value* and hide the others."""
        for f in self._frames.values():
            f.pack_forget()
        if value in self._frames:
            self._frames[value].pack(fill="both", expand=True)
            
            # Automatically focus the relevant field for operability
            if value == "Delete by Vehicle Number" and hasattr(self, 'del_car_entry'):
                self.after(50, self.del_car_entry.focus)

    def _delete_all(self):
        """Delete all records after confirmation."""
        if self.show_confirm(
            "Confirm", "Delete ALL records? This cannot be undone."
        ):
            try:
                self.db.delete_all_records()
                self.show_info("Done", "All records deleted.")
                self.app.broadcast_refresh()
            except Exception as exc:
                self.show_error("Error", str(exc))

    def _delete_by_date(self):
        """Delete records in the selected date range after confirmation."""
        f = self.del_from.get_date().strftime("%Y-%m-%d 00:00:00")
        t = self.del_to.get_date().strftime("%Y-%m-%d 23:59:59")
        if self.show_confirm(
            "Confirm", f"Delete records from {f[:10]} to {t[:10]}?"
        ):
            try:
                self.db.delete_records_by_date(f, t)
                self.show_info("Done", "Records deleted.")
                self.app.broadcast_refresh()
            except Exception as exc:
                self.show_error("Error", str(exc))

    def _delete_by_vehicle(self):
        """Delete records for the entered vehicle number after confirmation."""
        car = self.del_car.get().strip().upper()
        if not car:
            self.show_error("Input Required", "Enter a vehicle number.")
            return
        if self.show_confirm("Confirm", f"Delete all records for {car}?"):
            try:
                self.db.delete_records_by_car(car)
                self.show_info("Done", f"Records for {car} deleted.")
                self.del_car.set("")
                self.app.broadcast_refresh()
            except Exception as exc:
                self.show_error("Error", str(exc))
