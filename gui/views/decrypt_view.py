import flet as ft


def build_decrypt_view(show_main_view, file_picker, file_status, decrypt_btn):
    progress_bar = ft.ProgressBar(visible=False)
    password_field = ft.TextField(
        label="Decryption Key",
        password=True,
        can_reveal_password=True,
        width=300,
        hint_text="Exactly 9 characters required",
        on_change=lambda e: validate_password(e.control.value),
    )

    def validate_password(value):
        is_valid = len(value) == 9
        decrypt_btn.disabled = not is_valid or file_status.value == "No file selected"
        password_field.error_text = None if is_valid else "Password must be exactly 9 characters"
        password_field.update()
        decrypt_btn.update()

    def handle_click(_):
        if hasattr(decrypt_btn, '_handle_click'):
            decrypt_btn._handle_click(password_field.value, progress_bar)

    decrypt_btn.on_click = handle_click
    decrypt_btn.width = 300

    return ft.Column(
        controls=[
            ft.Container(
                content=ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: show_main_view()),
                    ft.Text("Decrypt File", size=24, weight=ft.FontWeight.BOLD),
                ]),
                margin=ft.margin.only(bottom=20),
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(height=80),
                        ft.ElevatedButton(
                            "Select Image",
                            icon=ft.Icons.UPLOAD_FILE,
                            on_click=lambda _: file_picker.pick_files(allowed_extensions=['jpg', 'jpeg']),
                            width=300,
                        ),
                        file_status,
                        password_field,
                        progress_bar,
                        decrypt_btn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            ),
        ],
        expand=True,
    )
