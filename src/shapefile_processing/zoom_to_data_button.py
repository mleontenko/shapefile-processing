from collections.abc import Callable

from PyQt6.QtCore import QEvent, QObject, QTimer
from PyQt6.QtWidgets import QPushButton
import pyqtgraph as pg


class ZoomToDataButton(QObject):
    def __init__(self, plot_widget: pg.PlotWidget, on_click: Callable[[], None]) -> None:
        super().__init__(plot_widget)
        self.plot_widget: pg.PlotWidget | None = plot_widget
        self.viewport = plot_widget.viewport()
        self.button = QPushButton('Zoom to Data', self.viewport)
        self.button.setAutoDefault(False)
        self.button.setDefault(False)
        self.button.setEnabled(False)
        self.button.clicked.connect(on_click)
        self.button.adjustSize()

        self.viewport.installEventFilter(self)
        plot_widget.destroyed.connect(self._clear_references)
        self.viewport.destroyed.connect(self._clear_references)

    def setEnabled(self, enabled: bool) -> None:
        self.button.setEnabled(enabled)

    def schedule_reposition(self) -> None:
        # run this on the next event loop cycle
        # after Qt finishing processing current events and updating the layout
        # this ensures the layout is ready
        QTimer.singleShot(0, self.reposition)

    # catches manual resize events
    def eventFilter(self, obj: QObject | None, event: QEvent | None) -> bool:
        if (
            obj is self.viewport
            and event is not None
            and event.type() == QEvent.Type.Resize
        ):
            self.reposition()
        return super().eventFilter(obj, event)

    def reposition(self) -> None:
        if self.plot_widget is None:
            return
        view_box = self.plot_widget.getPlotItem().getViewBox()
        scene_rect = view_box.sceneBoundingRect()
        bottom_right = self.plot_widget.mapFromScene(scene_rect.bottomRight())
        margin = 6
        self.button.move(
            bottom_right.x() - self.button.width() - margin,
            bottom_right.y() - self.button.height() - margin,
        )

    # cleanup to avoid errors if eventFilter() or reposition() runs during teardown
    def _clear_references(self) -> None:
        self.plot_widget = None
        self.viewport = None
