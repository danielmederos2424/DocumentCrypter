import sys
from pathlib import Path
from gui.app import EncryptionApp
import flet as ft

sys.path.append(str(Path(__file__).parent))


def main():
    app = EncryptionApp()
    ft.app(target=app.main)


if __name__ == '__main__':
    main()
