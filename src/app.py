"""Multi-window application coordinator.

Three independent windows (Entry, Exit, Admin Control) run simultaneously
and share a single Database instance.  After any DB write the calling
window broadcasts a refresh so every window updates its displayed data.
"""

import customtkinter

from src.config import load_settings
from src.database import Database


class ParkingApp:
    """Coordinator that owns shared state and the three top-level windows."""

    def __init__(self):
        # A hidden root is required by tkinter as the event-loop owner.
        self._root = customtkinter.CTk()
        self._root.withdraw()
        self._root.title("Parking System")

        self.settings = load_settings()
        self.db = Database()

        customtkinter.set_appearance_mode(self.settings["theme"])
        customtkinter.set_default_color_theme(self.settings["accent_color"])

        from src.screens.entry import EntryScreen
        from src.screens.exit_screen import ExitScreen
        from src.screens.owner import OwnerLogin

        # Cascade the three windows so they don't pile directly on top of each
        # other.  Offsets are (x, y) in pixels relative to the screen centre.
        configs = [
            ("Entry — Parking System",         EntryScreen,  (-330, -40)),
            ("Exit — Parking System",           ExitScreen,   (   0, -40)),
            ("Admin Control — Parking System",  OwnerLogin,   ( 330, -40)),
        ]

        self._windows: list["ParkingWindow"] = []
        for title, screen, offset in configs:
            win = ParkingWindow(self._root, self, title, screen, offset=offset)
            win.protocol("WM_DELETE_WINDOW", lambda w=win: self._on_close(w))
            self._windows.append(win)

    # ------------------------------------------------------------------
    # Event loop
    # ------------------------------------------------------------------

    def mainloop(self):
        """Start the tkinter event loop."""
        self._root.mainloop()

    # ------------------------------------------------------------------
    # Shared helpers – mirrored on every ParkingWindow so screens can call
    # self.app.get_font() / self.app.reload_settings() transparently.
    # ------------------------------------------------------------------

    def reload_settings(self):
        """Reload settings from disk and apply the theme."""
        self.settings = load_settings()
        customtkinter.set_appearance_mode(self.settings["theme"])

    def get_font(self, size_offset: int = 0, weight: str = "normal") -> tuple:
        """Return a font tuple based on the current settings."""
        return (
            self.settings["font_family"],
            self.settings["font_size"] + size_offset,
            weight,
        )

    # ------------------------------------------------------------------
    # Sync
    # ------------------------------------------------------------------

    def broadcast_refresh(self):
        """Ask every open window to refresh the screen it is currently showing.

        Call this after any database write (entry / exit) so all windows
        display up-to-date data without the operator having to switch away
        and back.
        """
        for win in self._windows:
            try:
                if win.winfo_exists():
                    win._refresh_current()
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Window lifecycle
    # ------------------------------------------------------------------

    def _on_close(self, win: "ParkingWindow"):
        """Destroy *win*; quit the application when no windows remain."""
        try:
            win.destroy()
        except Exception:
            pass
        alive = [w for w in self._windows if w.winfo_exists()]
        if not alive:
            self._quit()

    def _quit(self):
        try:
            self._root.destroy()
        except Exception:
            pass


# ---------------------------------------------------------------------------


class ParkingWindow(customtkinter.CTkToplevel):
    """A top-level window that manages its own screen stack.

    Each window receives a reference to the shared :class:`ParkingApp`
    coordinator so it can delegate ``db``, ``settings``, ``get_font()``,
    ``reload_settings()``, and ``broadcast_refresh()`` transparently.
    Screens still call ``self.app.*`` and receive a :class:`ParkingWindow`
    as ``app``, which forwards everything to the coordinator.
    """

    def __init__(
        self,
        master,
        coordinator: ParkingApp,
        title: str,
        initial_screen,
        offset: tuple[int, int] = (0, 0),
    ):
        super().__init__(master)
        self._coordinator = coordinator
        self.title(title)

        w, h = 900, 620
        self.geometry(f"{w}x{h}")
        self.minsize(700, 500)

        # Centre with offset so the three windows cascade nicely.
        self.update_idletasks()
        cx = (self.winfo_screenwidth()  // 2) - (w // 2) + offset[0]
        cy = (self.winfo_screenheight() // 2) - (h // 2) + offset[1]
        self.geometry(f"{w}x{h}+{cx}+{cy}")

        self.container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self._current_frame = None
        self.show_screen(initial_screen)

    # ------------------------------------------------------------------
    # Proxy properties – screens access these via self.app.*
    # ------------------------------------------------------------------

    @property
    def db(self) -> Database:
        return self._coordinator.db

    @property
    def settings(self) -> dict:
        return self._coordinator.settings

    def get_font(self, size_offset: int = 0, weight: str = "normal") -> tuple:
        return self._coordinator.get_font(size_offset, weight)

    def reload_settings(self):
        self._coordinator.reload_settings()

    def broadcast_refresh(self):
        """Called by a screen after a DB write to sync all windows."""
        self._coordinator.broadcast_refresh()

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def show_screen(self, screen_class, **kwargs):
        """Replace the current screen with *screen_class* inside this window."""
        if self._current_frame is not None:
            self._current_frame.destroy()
        self._current_frame = screen_class(self.container, self, **kwargs)
        self._current_frame.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # Sync
    # ------------------------------------------------------------------

    def _refresh_current(self):
        """Ask the current screen to refresh its data if it supports it."""
        if self._current_frame is not None and hasattr(self._current_frame, "refresh"):
            self._current_frame.refresh()
