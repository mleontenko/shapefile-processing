"""Dialog for editing runtime processing parameters used by toolbar actions."""

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)


class ParametersDialog(QDialog):
    """Modal dialog for editing ID prefix, neighbor radius, and outlier threshold."""

    def __init__(
        self,
        id_prefix: str,
        neighbor_radius: float,
        outlier_distance_threshold: float,
        parent=None,
    ) -> None:
        """Initialize dialog controls with current parameter values.

        Args:
            id_prefix (str): Current ID prefix used by assign IDs.
            neighbor_radius (float): Current radius used by neighbor counting.
            outlier_distance_threshold (float): Current distance threshold for outliers.
            parent: Optional Qt parent widget.
        """
        super().__init__(parent)
        self.setWindowTitle("Parameters")

        self._id_prefix: str = id_prefix
        self._neighbor_radius: float = neighbor_radius
        self._outlier_distance_threshold: float = outlier_distance_threshold

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("ID prefix for Assign IDs:"))
        self.prefix_input = QLineEdit(self)
        self.prefix_input.setText(id_prefix)
        layout.addWidget(self.prefix_input)

        layout.addWidget(QLabel("Radius for number of neighbors:"))
        self.radius_input = QLineEdit(self)
        self.radius_input.setText(str(neighbor_radius))
        layout.addWidget(self.radius_input)

        layout.addWidget(QLabel("Distance threshold for spatial outliers:"))
        self.threshold_input = QLineEdit(self)
        self.threshold_input.setText(str(outlier_distance_threshold))
        layout.addWidget(self.threshold_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            parent=self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept(self) -> None:
        """Validate entered values and close dialog if valid."""
        prefix = self.prefix_input.text().strip()
        if not prefix:
            QMessageBox.information(
                self,
                "Invalid Prefix",
                'Prefix cannot be empty. Use a value like "BLD_".',
            )
            return

        try:
            radius = float(self.radius_input.text().strip())
            threshold = float(self.threshold_input.text().strip())
        except ValueError:
            QMessageBox.information(
                self,
                "Invalid Parameters",
                "Radius and distance threshold must be numeric values.",
            )
            return

        if radius < 0 or threshold < 0:
            QMessageBox.information(
                self,
                "Invalid Parameters",
                "Radius and distance threshold must be non-negative values.",
            )
            return

        self._id_prefix = prefix
        self._neighbor_radius = radius
        self._outlier_distance_threshold = threshold
        super().accept()

    def get_values(self) -> tuple[str, float, float]:
        """Return validated parameter values from the dialog.

        Returns:
            tuple[str, float, float]: ID prefix, neighbor radius, and outlier threshold.
        """
        return self._id_prefix, self._neighbor_radius, self._outlier_distance_threshold
