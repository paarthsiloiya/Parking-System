"""UI settings screen (font, theme, accent colour, etc.)."""

import customtkinter
from tkinter import StringVar
import tkinter.font as tkfont

from src.screens.base import BaseScreen
from src.config import load_settings, save_settings


class SettingsScreen(BaseScreen):
    """Edit UI preferences (font, theme, accent colour, etc.)."""

    def __init__(self, parent, app):
        """Build and display the settings form."""
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        """Lay out font, theme, and accent fields with a save button."""
        from src.screens.main_menu import MainMenu

        back = self.create_back_button(self, MainMenu)
        back.pack(anchor="nw", padx=10, pady=10)

        customtkinter.CTkLabel(
            self, text="Settings",
            font=self.get_font(size_offset=8, weight="bold"),
        ).pack(pady=(5, 15))

        form = customtkinter.CTkFrame(self, fg_color="transparent")
        form.pack(pady=10)

        s = load_settings()
        fonts = sorted({f for f in tkfont.families() if not f.startswith("@")})

        rows: list[tuple[str, str, customtkinter.CTkBaseClass]] = []

        self.font_family = StringVar(value=s["font_family"])
        self.font_size = StringVar(value=str(s["font_size"]))
        self.theme = StringVar(value=s["theme"])
        self.accent = StringVar(value=s["accent_color"])
        self.radius = StringVar(value=str(s["corner_radius"]))
        self.border = StringVar(value=str(s["border_width"]))

        field_defs = [
            ("Font Family:", self.font_family, "option", fonts),
            ("Font Size:",   self.font_size,   "entry",  None),
            ("Theme:",       self.theme,        "option", ["System", "Light", "Dark"]),
            ("Accent Color:", self.accent,      "option", ["blue", "green", "dark-blue"]),
            ("Corner Radius:", self.radius,     "entry",  None),
            ("Border Width:", self.border,       "entry",  None),
        ]

        for row, (label, var, kind, values) in enumerate(field_defs):
            customtkinter.CTkLabel(
                form, text=label, font=self.get_font()
            ).grid(row=row, column=0, padx=10, pady=8, sticky="e")

            if kind == "option" and values:
                customtkinter.CTkOptionMenu(
                    form, values=values, variable=var,
                    font=self.get_font(), dropdown_font=self.get_font(),
                    width=220,
                ).grid(row=row, column=1, padx=10, pady=8)
            else:
                customtkinter.CTkEntry(
                    form, textvariable=var, width=220, font=self.get_font(),
                ).grid(row=row, column=1, padx=10, pady=8)

        customtkinter.CTkButton(
            form, text="Save Settings",
            font=self.get_font(weight="bold"),
            command=self._save,
        ).grid(
            row=len(field_defs), column=0, columnspan=2,
            pady=20, sticky="ew", padx=10,
        )

        customtkinter.CTkLabel(
            self,
            text="Note: Restart the app for theme / accent changes to fully apply.",
            font=self.get_font(size_offset=-2), text_color="gray",
        ).pack(pady=5)

    def _save(self):
        """Validate numeric fields and persist the updated settings."""
        try:
            fs = int(self.font_size.get())
            cr = int(self.radius.get())
            bw = int(self.border.get())
        except ValueError:
            self.show_error(
                "Invalid Input",
                "Font size, corner radius and border width must be integers.",
            )
            return

        new = {
            "font_family": self.font_family.get(),
            "font_size": fs,
            "theme": self.theme.get(),
            "accent_color": self.accent.get(),
            "corner_radius": cr,
            "border_width": bw,
        }

        save_settings(new)
        self.app.reload_settings()
        customtkinter.set_appearance_mode(new["theme"])
        self.show_info("Saved", "Settings saved. Some changes require a restart.")
