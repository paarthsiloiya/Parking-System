"""Bill display dialog (shown after vehicle exit)."""

import customtkinter


class BillDialog(customtkinter.CTkToplevel):
    """Modal dialog that shows the parking bill."""

    def __init__(self, parent, bill_data: dict, app):
        """Create the bill dialog and populate it with *bill_data*.

        :param parent: Parent widget.
        :param bill_data: Dictionary with keys ``car_no``, ``vehicle_type``,
            ``token_number``, ``entry_time``, ``exit_time``, ``slot``,
            and ``bill``.
        :param app: The :class:`~src.app.ParkingApp` instance.
        """
        super().__init__(parent)
        self.title("Parking Bill")
        self.geometry("420x380")
        self.resizable(False, False)

        x = (self.winfo_screenwidth() // 2) - 210
        y = (self.winfo_screenheight() // 2) - 190
        self.geometry(f"420x380+{x}+{y}")

        font = app.get_font()
        bold = app.get_font(weight="bold")
        title_font = app.get_font(size_offset=6, weight="bold")

        customtkinter.CTkLabel(
            self, text="PARKING BILL", font=title_font
        ).pack(pady=(20, 15))

        details = customtkinter.CTkFrame(self)
        details.pack(padx=20, pady=5, fill="x")

        fields = [
            ("Vehicle No:", bill_data.get("car_no", "")),
            ("Vehicle Type:", bill_data.get("vehicle_type", "")),
            ("Token:", str(bill_data.get("token_number", ""))),
            ("Entry Time:", bill_data.get("entry_time", "")),
            ("Exit Time:", bill_data.get("exit_time", "")),
            ("Slot:", bill_data.get("slot", "")),
        ]

        for i, (label, value) in enumerate(fields):
            customtkinter.CTkLabel(
                details, text=label, font=font, anchor="e"
            ).grid(row=i, column=0, padx=(15, 5), pady=4, sticky="e")
            customtkinter.CTkLabel(
                details, text=value, font=font, anchor="w"
            ).grid(row=i, column=1, padx=(5, 15), pady=4, sticky="w")

        total_frame = customtkinter.CTkFrame(self)
        total_frame.pack(padx=20, pady=10, fill="x")

        customtkinter.CTkLabel(
            total_frame, text="Total Amount:", font=bold
        ).grid(row=0, column=0, padx=15, pady=10, sticky="e")

        bill_amount = bill_data.get("bill", 0)
        customtkinter.CTkLabel(
            total_frame,
            text=f"\u20B9{bill_amount:,.2f}",
            font=app.get_font(size_offset=6, weight="bold"),
        ).grid(row=0, column=1, padx=15, pady=10, sticky="w")

        close_btn = customtkinter.CTkButton(
            self, text="Close", font=font, command=self.destroy
        )
        close_btn.pack(pady=15)
        
        self.bind("<Return>", lambda _: self.destroy())
        self.bind("<Escape>", lambda _: self.destroy())

        self.grab_set()
        self.focus_force()
        close_btn.focus()
