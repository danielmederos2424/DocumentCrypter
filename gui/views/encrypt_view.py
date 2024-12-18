import flet as ft


def build_encrypt_view(show_main_view, file_picker, file_status, encrypt_btn):
    progress_bar = ft.ProgressBar(visible=False)
    password_field = ft.TextField(
        label="Encryption Key",
        password=True,
        can_reveal_password=True,
        width=300,
        hint_text="Exactly 9 characters required",
        on_change=lambda e: validate_password(e.control.value),
    )

    def validate_password(value):
        is_valid = len(value) == 9
        encrypt_btn.disabled = not is_valid or file_status.value == "No file selected"
        password_field.error_text = None if is_valid else "Password must be exactly 9 characters"
        password_field.update()
        encrypt_btn.update()

    def handle_click(_):
        if hasattr(encrypt_btn, '_handle_click'):
            encrypt_btn._handle_click(password_field.value, progress_bar)

    encrypt_btn.on_click = handle_click
    encrypt_btn.width = 300

    return ft.Column(
        controls=[
            ft.Container(
                content=ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: show_main_view()),
                    ft.Text("Encrypt File", size=24, weight=ft.FontWeight.BOLD),
                ]),
                margin=ft.margin.only(bottom=20),
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(height=80),
                        ft.ElevatedButton(
                            "Select File",
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=lambda _: file_picker.pick_files(
                                allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']
                            ),
                            width=300,
                        ),
                        file_status,
                        password_field,
                        progress_bar,
                        encrypt_btn,
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
