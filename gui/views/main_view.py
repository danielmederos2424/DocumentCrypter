import flet as ft


def build_main_view(show_encrypt_view, show_decrypt_view):
    return ft.Column(
        controls=[
            ft.Text("Encryption/Decryption Utility", size=32, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Encrypt Document",
                        icon=ft.icons.LOCK,
                        on_click=lambda _: show_encrypt_view(),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=ft.padding.all(20),
                        ),
                        width=200,
                        height=60,
                    ),
                    ft.ElevatedButton(
                        "Decrypt Image",
                        icon=ft.icons.LOCK_OPEN,
                        on_click=lambda _: show_decrypt_view(),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=ft.padding.all(20),
                        ),
                        width=200,
                        height=60,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40,
        expand=True,
    )
