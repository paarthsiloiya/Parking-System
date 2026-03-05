"""Base screen class — every screen inherits from this."""

import os
from tkinter import messagebox

import customtkinter
from PIL import Image

from src.config import ICONS_DIR


class BaseScreen(customtkinter.CTkFrame):
    """Provides shared helpers for all screens."""

    def __init__(self, parent, app, **kwargs):
        """Initialise the base screen.

        :param parent: Parent widget (usually the app container).
        :param app: The :class:`~src.app.ParkingApp` instance.
        """
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.app = app
        self.db = app.db
        
        # Unbind Escape by default to prevent leftover bindings from previous screens
        try:
            self.winfo_toplevel().unbind("<Escape>")
        except Exception:
            pass

    @property
    def settings(self) -> dict:
        """Return the current application settings dictionary."""
        return self.app.settings

    def get_font(self, size_offset=0, weight="normal"):
        """Return a font tuple based on the current settings.

        :param size_offset: Points to add to the base font size.
        :param weight: ``'normal'`` or ``'bold'``.
        :returns: Tuple of ``(family, size, weight)``.
        """
        return self.app.get_font(size_offset, weight)

    def load_icon(self, filename: str, size: tuple[int, int] = (30, 30)):
        """Load a single icon file. Returns *None* if missing."""
        path = os.path.join(ICONS_DIR, filename)
        if not os.path.exists(path):
            return None
        try:
            img = Image.open(path)
            return customtkinter.CTkImage(
                light_image=img, dark_image=img, size=size
            )
        except Exception:
            return None

    def load_themed_icon(
        self, base_name: str, size: tuple[int, int] = (30, 30)
    ):
        """Load icon with automatic light/dark variants.

        Looks for ``<base_name> black.png`` (light mode) and
        ``<base_name> white.png`` (dark mode).
        """
        light_path = os.path.join(ICONS_DIR, f"{base_name} black.png")
        dark_path = os.path.join(ICONS_DIR, f"{base_name} white.png")

        light_img = Image.open(light_path) if os.path.exists(light_path) else None
        dark_img = Image.open(dark_path) if os.path.exists(dark_path) else None

        if light_img is None and dark_img is None:
            return None

        return customtkinter.CTkImage(
            light_image=light_img or dark_img,
            dark_image=dark_img or light_img,
            size=size,
        )

    def create_back_button(self, parent, target_screen):
        """Return a ← Back button that navigates to *target_screen*."""
        try:
            self.winfo_toplevel().bind("<Escape>", lambda e: self.app.show_screen(target_screen))
        except Exception:
            pass

        return customtkinter.CTkButton(
            parent,
            text="← Back (Esc)",
            font=self.get_font(),
            width=100,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            anchor="w",
            command=lambda: self.app.show_screen(target_screen),
        )

    def show_error(self, title: str, message: str):
        """Display an error message box.

        :param title: Dialog title.
        :param message: Error message text.
        """
        messagebox.showerror(title, message)

    def show_info(self, title: str, message: str):
        """Display an informational message box.

        :param title: Dialog title.
        :param message: Information text.
        """
        messagebox.showinfo(title, message)

    def show_confirm(self, title: str, message: str) -> bool:
        """Display a yes/no confirmation dialog.

        :param title: Dialog title.
        :param message: Confirmation question.
        :returns: ``True`` if the user clicked *Yes*.
        """
        return messagebox.askyesno(title, message, default="no")
