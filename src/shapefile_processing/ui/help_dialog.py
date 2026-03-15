"""Help dialog showing basic usage instructions for the application."""

from PyQt6.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QWidget


class HelpDialog(QDialog):
    """Modal dialog that displays app usage instructions."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize dialog layout and instruction text.

        Args:
            parent (QWidget | None): Optional parent widget.
        """
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.resize(700, 480)

        layout = QVBoxLayout(self)
        text_box = QTextEdit(self)
        text_box.setReadOnly(True)
        text_box.setPlainText(
            "Shapefile Processing - Quick Instructions\n\n"
            "1) Load data\n"
            "   - File -> Load Shapefile\n"
            "   - Select a .shp file.\n\n"
            "2) Optional: Set parameters or leave default\n"
            "   - Toolbar -> Parameters\n"
            "   - Configure ID prefix, neighbor radius, and outlier threshold.\n\n"
            "3) Run processing steps in suggested order\n"
            "   - 1. Assign IDs\n"
            "   - 2. Calculate Spatial Attributes\n"
            "   - 3. Data Quality Checks\n\n"
            "4) Inspect results\n"
            "   - View -> Attribute Table\n"
            "   - Use the map to inspect geometry and labels.\n\n"
            "5) Export output\n"
            "   - File -> Export Shapefile\n"
            "   - Save processed results as a new .shp file.\n\n"
            "Notes\n"
            "- Metrics (area/distance) depend on CRS units.\n"
            "- For meaningful metric values, use a projected CRS."
        )
        layout.addWidget(text_box)
