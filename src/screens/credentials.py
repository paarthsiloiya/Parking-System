"""Change owner credentials screen."""

import customtkinter
from tkinter import StringVar

from src.screens.base import BaseScreen
from src.config import (
    load_credentials, save_credentials,
    hash_password, verify_password,
)


class CredentialsScreen(BaseScreen):
    """Form for changing the owner username and/or password."""

    def __init__(self, parent, app):
        """Build and display the credentials form."""
        super().__init__(parent, app)
        self._create_widgets()

    def _create_widgets(self):
        """Lay out current-password, new-username, new-password inputs."""
        from src.screens.owner import OwnerMenu

        back = self.create_back_button(self, OwnerMenu)
        back.pack(anchor="nw", padx=10, pady=10)

        customtkinter.CTkLabel(
            self, text="Change Credentials",
            font=self.get_font(size_offset=8, weight="bold"),
        ).pack(pady=(10, 25))

        form = customtkinter.CTkFrame(self, fg_color="transparent")
        form.pack(pady=10)

        cr = self.settings["corner_radius"]
        bw = self.settings["border_width"]

        labels_entries = [
            ("Current Password:", True),
            ("New Username:",     False),
            ("New Password:",     True),
            ("Confirm Password:", True),
        ]

        self._vars: list[StringVar] = []
        for row, (label, is_password) in enumerate(labels_entries):
            customtkinter.CTkLabel(
                form, text=label, font=self.get_font()
            ).grid(row=row, column=0, padx=10, pady=8, sticky="e")

            var = StringVar()
            self._vars.append(var)
            customtkinter.CTkEntry(
                form, textvariable=var, width=260,
                font=self.get_font(), corner_radius=cr, border_width=bw + 1,
                show="•" if is_password else "",
            ).grid(row=row, column=1, padx=10, pady=8)

        customtkinter.CTkLabel(
            form,
            text="Leave username or password blank to keep current value.",
            font=self.get_font(size_offset=-2), text_color="gray",
        ).grid(row=len(labels_entries), column=0, columnspan=2, pady=5)

        icon = self.load_icon("finalChangeUsername.png")
        customtkinter.CTkButton(
            form, text="Update Credentials", image=icon,
            font=self.get_font(weight="bold"),
            corner_radius=cr, border_width=bw,
            command=self._update,
        ).grid(
            row=len(labels_entries) + 1, column=0, columnspan=2,
            pady=20, sticky="ew", padx=10,
        )

    def _update(self):
        """Verify current password and apply credential changes."""
        current_pass, new_user, new_pass, confirm_pass = (
            v.get() for v in self._vars
        )

        creds = load_credentials()
        if not verify_password(current_pass, creds["password_hash"]):
            self.show_error("Auth Failed", "Current password is incorrect.")
            return

        new_user = new_user.strip()
        if not new_user and not new_pass:
            self.show_error("No Changes", "Enter a new username or password.")
            return

        if new_pass and new_pass != confirm_pass:
            self.show_error("Mismatch", "New password and confirmation differ.")
            return

        if new_user:
            creds["username"] = new_user
        if new_pass:
            creds["password_hash"] = hash_password(new_pass)

        save_credentials(creds)
        self.show_info("Success", "Credentials updated successfully.")

        for v in self._vars:
            v.set("")
