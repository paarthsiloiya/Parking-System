"""Main application window and screen navigation."""

import customtkinter

from src.config import load_settings
from src.database import Database


class ParkingApp(customtkinter.CTk):
    """Root window that manages screen navigation."""

    def __init__(self):
        super().__init__()

        self.settings = load_settings()
        self.db = Database()

        customtkinter.set_appearance_mode(self.settings["theme"])
        customtkinter.set_default_color_theme(self.settings["accent_color"])

        self.title("Parking System")
        self.geometry("900x620")
        self.minsize(700, 500)

        self.update_idletasks()
        w, h = 900, 620
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        self.container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self._current_frame = None

        from src.screens.main_menu import MainMenu
        self.show_screen(MainMenu)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def show_screen(self, screen_class, **kwargs):
        """Destroy the current screen and display *screen_class*."""
        if self._current_frame is not None:
            self._current_frame.destroy()
        self._current_frame = screen_class(self.container, self, **kwargs)
        self._current_frame.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # Helpers exposed to screens
    # ------------------------------------------------------------------

    def reload_settings(self):
        """Reload settings from disk and apply the theme."""
        self.settings = load_settings()
        customtkinter.set_appearance_mode(self.settings["theme"])

    def get_font(self, size_offset=0, weight="normal"):
        """Return a font tuple based on the current settings."""
        return (
            self.settings["font_family"],
            self.settings["font_size"] + size_offset,
            weight,
        )
