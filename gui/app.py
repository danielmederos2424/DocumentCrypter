import flet as ft
from datetime import datetime
import threading
from PIL import Image
import os

from gui.views.main_view import build_main_view
from gui.views.encrypt_view import build_encrypt_view
from gui.views.decrypt_view import build_decrypt_view
from crypto.handler import CryptoHandler


class EncryptionApp:
    def __init__(self):
        self.crypto = CryptoHandler()
        self.page = None
        self.content = None
        self.file_picker = None
        self.current_file = None
        self._reset_view_state()

    def _reset_view_state(self):
        self.encrypt_btn = None
        self.file_status = None
        self.current_file = None

    def main(self, page: ft.Page):
        self.page = page
        page.title = "Encryption/Decryption Utility"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 20
        page.window.width = 800
        page.window.height = 600
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.content = ft.Container(
            content=build_main_view(self.show_encrypt_view, self.show_decrypt_view),
            expand=True,
            alignment=ft.alignment.center,
        )
        page.add(self.content)

    def show_snackbar(self, message: str, color: str = "error"):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()

    def validate_input(self, file_path: str, password: str) -> bool:
        if not file_path:
            self.show_snackbar("Please select a file")
            return False

        if not password:
            self.show_snackbar("Please enter an encryption key")
            return False

        if not self.crypto.validate_file_size(file_path):
            self.show_snackbar("File size exceeds 5MB limit")
            return False

        return True

    def handle_encryption(self, file_path: str, password: str, progress_bar: ft.ProgressBar):
        if not self.validate_input(file_path, password):
            return

        if len(password) != 9:
            self.show_snackbar("Password must be exactly 9 characters")
            return

        progress_bar.visible = True
        self.page.update()

        def update_progress(value):
            progress_bar.value = value
            self.page.update()

        def encrypt_task():
            try:
                encrypted_data, success = self.crypto.encrypt_file(file_path, password, update_progress)
                if not success:
                    self.show_snackbar(f"Encryption failed: {encrypted_data}")
                    return

                output_dir = os.path.dirname(file_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                original_ext = os.path.splitext(file_path)[1]
                output_path = os.path.join(output_dir, f"encrypted_{timestamp}_{original_ext[1:]}.jpg")

                img = self.crypto.data_to_image(encrypted_data)
                img.save(output_path, "JPEG")

                self.show_snackbar(f"File encrypted and saved as {os.path.basename(output_path)}", "green")

            except Exception as e:
                self.show_snackbar(f"Error: {str(e)}")
            finally:
                progress_bar.visible = False
                self.page.update()

        threading.Thread(target=encrypt_task, daemon=True).start()

    def show_encrypt_view(self):
        self._reset_view_state()
        self.file_picker = ft.FilePicker(on_result=self.handle_file_picked)
        self.page.overlay.clear()
        self.page.overlay.append(self.file_picker)

        self.file_status = ft.Text("No file selected", color="error", size=14)
        self.encrypt_btn = ft.ElevatedButton("Encrypt", icon=ft.Icons.LOCK, disabled=True)
        self.encrypt_btn._handle_click = lambda pwd, pb: self.handle_encryption(self.current_file, pwd, pb)

        self.encrypt_view = build_encrypt_view(
            self.show_main_view,
            self.file_picker,
            self.file_status,
            self.encrypt_btn
        )

        self.content.content = self.encrypt_view
        self.page.update()

    def handle_file_picked(self, e):
        if not e.files:
            return

        self.current_file = e.files[0].path

        if hasattr(self, 'encrypt_btn') and self.encrypt_btn:
            self.file_status.value = f"Selected: {os.path.basename(self.current_file)}"
            self.file_status.color = "green"
            self.encrypt_btn.disabled = False
        elif hasattr(self, 'decrypt_btn') and self.decrypt_btn:
            self.file_status.value = f"Selected: {os.path.basename(self.current_file)}"
            self.file_status.color = "green"
            self.decrypt_btn.disabled = False

        self.content.update()
        self.page.update()

    def show_main_view(self):
        self.content.content = build_main_view(self.show_encrypt_view, self.show_decrypt_view)
        self.page.update()

    def show_decrypt_view(self):
        self._reset_view_state()
        self.file_picker = ft.FilePicker(on_result=self.handle_file_picked)
        self.page.overlay.clear()
        self.page.overlay.append(self.file_picker)

        self.file_status = ft.Text("No file selected", color="error", size=14)
        self.decrypt_btn = ft.ElevatedButton("Decrypt", icon=ft.Icons.LOCK_OPEN, disabled=True)
        self.decrypt_btn._handle_click = lambda pwd, pb: self.handle_decryption(self.current_file, pwd, pb)

        self.decrypt_view = build_decrypt_view(
            self.show_main_view,
            self.file_picker,
            self.file_status,
            self.decrypt_btn
        )

        self.content.content = self.decrypt_view
        self.page.update()

    def handle_decryption(self, file_path: str, password: str, progress_bar: ft.ProgressBar):
        if not self.validate_input(file_path, password):
            return

        if len(password) != 9:
            self.show_snackbar("Password must be exactly 9 characters")
            return

        progress_bar.visible = True
        self.page.update()

        def update_progress(value):
            progress_bar.value = value
            self.page.update()

        def decrypt_task():
            try:
                img = Image.open(file_path)
                encrypted_data = self.crypto.image_to_data(img)

                # Extract original extension from filename
                filename = os.path.basename(file_path)
                ext_part = filename.split('_')[-1].split('.')[0]  # Gets extension between last underscore and .jpg
                original_ext = f".{ext_part}"

                decrypted_data, success = self.crypto.decrypt_file(
                    encrypted_data,
                    password,
                    original_ext,
                    update_progress
                )

                if not success:
                    self.show_snackbar(f"Decryption failed: {decrypted_data}")
                    return

                output_dir = os.path.dirname(file_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(output_dir, f"decrypted_{timestamp}{original_ext}")

                with open(output_path, 'wb') as f:
                    f.write(decrypted_data)

                self.show_snackbar(f"File decrypted and saved as {os.path.basename(output_path)}", "green")

            except Exception as e:
                self.show_snackbar(f"Error: {str(e)}")
            finally:
                progress_bar.visible = False
                self.page.update()

        threading.Thread(target=decrypt_task, daemon=True).start()
