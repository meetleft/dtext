import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from editor.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("TextEditMac")
    app.setOrganizationName("TextEditMac")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
