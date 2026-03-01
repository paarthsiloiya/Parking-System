"""Main menu screen — Entry, Exit, Owner, Settings."""

import customtkinter

from src.screens.base import BaseScreen


class MainMenu(BaseScreen):
    """Main menu with Entry, Exit, Owner, and Settings buttons."""

    def __init__(self, parent, app):
        """Build and display the main menu."""
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        """Lay out the main menu UI elements."""
        top_bar = customtkinter.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=10, pady=(10, 0))

        settings_icon = self.load_themed_icon("settings", (20, 20))
        settings_btn = customtkinter.CTkButton(
            top_bar,
            text="Settings",
            image=settings_icon,
            font=self.get_font(size_offset=-2),
            width=100,
            height=30,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            command=self._open_settings,
        )
        settings_btn.pack(side="right")

        header = customtkinter.CTkLabel(
            self,
            text="🅿  Parking System",
            font=self.get_font(size_offset=14, weight="bold"),
        )
        header.pack(pady=(30, 5))

        subtitle = customtkinter.CTkLabel(
            self,
            text="Vehicle Parking Management System",
            font=self.get_font(size_offset=2),
            text_color="gray",
        )
        subtitle.pack(pady=(0, 40))

        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        entry_icon = self.load_themed_icon("login mainchoice", (80, 80))
        exit_icon = self.load_themed_icon("exit mainchoice", (80, 80))
        owner_icon = self.load_themed_icon("owner mainchoice", (80, 80))

        cr = self.settings["corner_radius"]
        bw = self.settings["border_width"]

        for col, (text, icon, cmd) in enumerate(
            [
                ("ENTRY", entry_icon, self._open_entry),
                ("EXIT", exit_icon, self._open_exit),
                ("OWNER", owner_icon, self._open_owner),
            ]
        ):
            btn = customtkinter.CTkButton(
                btn_frame,
                text=text,
                image=icon,
                compound="top",
                font=self.get_font(size_offset=2, weight="bold"),
                width=160,
                height=140,
                corner_radius=cr,
                border_width=bw,
                command=cmd,
            )
            btn.grid(row=0, column=col, padx=20, pady=10)

        footer = customtkinter.CTkLabel(
            self,
            text="Parking System  •  v2.0",
            font=self.get_font(size_offset=-3),
            text_color="gray",
        )
        footer.pack(side="bottom", pady=10)

    def _open_entry(self):
        """Navigate to the vehicle entry screen."""
        from src.screens.entry import EntryScreen
        self.app.show_screen(EntryScreen)

    def _open_exit(self):
        """Navigate to the vehicle exit screen."""
        from src.screens.exit_screen import ExitScreen
        self.app.show_screen(ExitScreen)

    def _open_owner(self):
        """Navigate to the owner login screen."""
        from src.screens.owner import OwnerLogin
        self.app.show_screen(OwnerLogin)

    def _open_settings(self):
        """Navigate to the settings screen."""
        from src.screens.settings_screen import SettingsScreen
        self.app.show_screen(SettingsScreen)
