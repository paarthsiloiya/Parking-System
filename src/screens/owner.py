"""Owner login gate and management menu."""

import customtkinter
from tkinter import StringVar

from src.screens.base import BaseScreen
from src.config import load_credentials, verify_password


class OwnerLogin(BaseScreen):
    """Password gate before the owner menu."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        customtkinter.CTkLabel(
            self, text="Owner Login",
            font=self.get_font(size_offset=8, weight="bold"),
        ).pack(pady=(30, 30))

        form = customtkinter.CTkFrame(self, fg_color="transparent")
        form.pack(pady=10)

        cr = self.settings["corner_radius"]

        customtkinter.CTkLabel(
            form, text="Username:", font=self.get_font()
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.username = StringVar()
        user_entry = customtkinter.CTkEntry(
            form, textvariable=self.username, width=250,
            font=self.get_font(), corner_radius=cr,
        )
        user_entry.grid(row=0, column=1, padx=10, pady=10)


        customtkinter.CTkLabel(
            form, text="Password:", font=self.get_font()
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.password = StringVar()
        pass_entry = customtkinter.CTkEntry(
            form, textvariable=self.password, width=250,
            font=self.get_font(), show="•", corner_radius=cr,
        )
        pass_entry.grid(row=1, column=1, padx=10, pady=10)


        icon = self.load_icon("login.png")
        customtkinter.CTkButton(
            form, text="Login", image=icon,
            font=self.get_font(weight="bold"),
            corner_radius=cr,
            command=self._login,
        ).grid(row=2, column=0, columnspan=2, pady=20, sticky="ew", padx=10)

        user_entry.bind("<Return>", lambda _: pass_entry.focus())
        pass_entry.bind("<Return>", lambda _: self._login())

    def _login(self):
        """Verify credentials and navigate to the owner menu on success."""
        creds = load_credentials()
        if (
            self.username.get().strip() == creds["username"]
            and verify_password(self.password.get(), creds["password_hash"])
        ):
            self.app.show_screen(OwnerMenu)
        else:
            self.show_error("Login Failed", "Incorrect username or password.")
            self.password.set("")


class OwnerMenu(BaseScreen):
    """Dashboard with buttons for every management action."""

    def __init__(self, parent, app):
        """Build and display the owner management menu."""
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        """Create the scrollable list of management buttons."""
        # Re-lock: navigating back takes the operator to the login screen.
        back = self.create_back_button(self, OwnerLogin)
        back.pack(anchor="nw", padx=10, pady=10)

        customtkinter.CTkLabel(
            self, text="Owner Panel",
            font=self.get_font(size_offset=8, weight="bold"),
        ).pack(pady=(5, 15))

        frame = customtkinter.CTkScrollableFrame(self, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=40, pady=10)

        cr = self.settings["corner_radius"]
        bw = self.settings["border_width"]
        btn_w = 460

        items = [
            ("Change Credentials",    "change-user.png",    self._go_credentials),
            ("View Records",          "viewRec.png",        self._go_records),
            ("Delete Records",        "delRec.png",         self._go_delete),
            ("Change Vehicle Options", "parking.png",       self._go_options),
            ("View Income",           "income.png",         self._go_income),
            ("Change Pricing",        "changeAmount.png",   self._go_pricing),
            ("Manage Parking Slots",  "parkingAlt.png",     self._go_slots),
            ("Settings",              "settings.png",       self._go_settings),
        ]

        for text, icon_name, cmd in items:
            icon = self.load_icon(icon_name)
            customtkinter.CTkButton(
                frame, text=text, image=icon,
                font=self.get_font(), width=btn_w,
                corner_radius=cr, border_width=bw,
                command=cmd,
            ).pack(pady=5, ipady=5)

    def _go_credentials(self):
        """Navigate to the credentials screen."""
        from src.screens.credentials import CredentialsScreen
        self.app.show_screen(CredentialsScreen)

    def _go_records(self):
        """Navigate to the records screen."""
        from src.screens.records import RecordsScreen
        self.app.show_screen(RecordsScreen)

    def _go_delete(self):
        """Navigate to the delete records screen."""
        from src.screens.delete_records import DeleteRecordsScreen
        self.app.show_screen(DeleteRecordsScreen)

    def _go_options(self):
        """Navigate to the vehicle options screen."""
        from src.screens.vehicle_options import VehicleOptionsScreen
        self.app.show_screen(VehicleOptionsScreen)

    def _go_income(self):
        """Navigate to the income screen."""
        from src.screens.income import IncomeScreen
        self.app.show_screen(IncomeScreen)

    def _go_pricing(self):
        """Navigate to the pricing screen."""
        from src.screens.pricing import PricingScreen
        self.app.show_screen(PricingScreen)

    def _go_slots(self):
        """Navigate to the slots management screen."""
        from src.screens.slots import SlotsScreen
        self.app.show_screen(SlotsScreen)

    def _go_settings(self):
        """Navigate to the settings screen."""
        from src.screens.settings_screen import SettingsScreen
        self.app.show_screen(SettingsScreen)
