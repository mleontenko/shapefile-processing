"""Entry point for launching the shapefile-processing desktop application."""

import sys

from PyQt6.QtWidgets import QApplication

from shapefile_processing.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
