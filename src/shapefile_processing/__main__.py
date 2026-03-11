import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)
import pyqtgraph as pg

from shapefile_processing.shapefile_manager import ShapefileManager

pg.setConfigOptions(antialias=True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Shapefile Loader')
        self.setGeometry(100, 100, 800, 600)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.08)
        self.plot_widget.setAspectLocked(True)
        
        # Format axes to show full decimal notation instead of scientific
        ax_x = self.plot_widget.getAxis('bottom')
        ax_y = self.plot_widget.getAxis('left')
        ax_x.tickStrings = lambda values, scale, spacing: [f'{int(v)}' for v in values]
        ax_y.tickStrings = lambda values, scale, spacing: [f'{int(v)}' for v in values]

        self.shapefile_manager = ShapefileManager(self.plot_widget)
        
        self.setCentralWidget(self.plot_widget)

        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        view_menu = menu_bar.addMenu('View')

        load_action = QAction('Load Shapefile', self)
        load_action.triggered.connect(self.load_shapefile)
        file_menu.addAction(load_action)

        attribute_table_action = QAction('Attribute Table', self)
        attribute_table_action.triggered.connect(self.show_attribute_table)
        view_menu.addAction(attribute_table_action)

    def load_shapefile(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            'Load Shapefile',
            '',
            'Shapefiles (*.shp);;All Files (*)',
        )
        if file_name:
            self.render_shapefile(file_name)

    def render_shapefile(self, file_name):
        try:
            has_features = self.shapefile_manager.load_and_render(file_name)
        except Exception as error:
            QMessageBox.critical(self, 'Load Error', f'Failed to load shapefile:\n{error}')
            return

        if not has_features:
            QMessageBox.information(self, 'Empty Layer', 'The selected shapefile contains no features.')
            return

    def show_attribute_table(self):
        attributes = self.shapefile_manager.get_attributes()
        if attributes is None:
            QMessageBox.information(self, 'No Layer Loaded', 'Please load a shapefile first.')
            return

        table_dialog = QDialog(self)
        table_dialog.setWindowTitle('Attribute Table')
        table_dialog.resize(900, 500)

        layout = QVBoxLayout(table_dialog)
        table_widget = QTableWidget(table_dialog)
        layout.addWidget(table_widget)

        table_widget.setRowCount(len(attributes))
        table_widget.setColumnCount(len(attributes.columns))
        table_widget.setHorizontalHeaderLabels([str(col) for col in attributes.columns])

        for row_index, (_, row_data) in enumerate(attributes.iterrows()):
            for col_index, value in enumerate(row_data):
                display_value = '' if value is None else str(value)
                table_widget.setItem(row_index, col_index, QTableWidgetItem(display_value))

        table_widget.resizeColumnsToContents()
        table_dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())