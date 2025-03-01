import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QImage, QPixmap, QColor
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from gui.gui import Ui_Widget


QtCore.QLocale.setDefault(QtCore.QLocale(
    QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates))


class MyApp(QtWidgets.QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.points = []
        self.setupUi(self)

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QtGui.QColor(255, 255, 255))
        self.graphicsView.setScene(self.scene)

        double_validator = QtGui.QDoubleValidator()
        double_validator.setBottom(-float('inf'))
        double_validator.setTop(float('inf'))
        double_validator.setNotation(
        QtGui.QDoubleValidator.Notation.StandardNotation)
        double_validator.setLocale(QtCore.QLocale("C"))

        self.dx_line.setValidator(double_validator)
        self.dy_line.setValidator(double_validator)
        self.angle_edit.setValidator(double_validator)
        self.coef_edit.setValidator(double_validator)

def run_gui_app():
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
