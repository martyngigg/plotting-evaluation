# coding: utf-8
from __future__ import print_function

import sip
sip.setapi('QString', 2)

from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4.QtGui import QApplication, QTableWidgetItem
from PyQt4.uic import loadUiType

from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

import numpy as np

# Process .ui file
Ui_MainWindow, QMainWindow = loadUiType('mainwindow.ui')

# Load 2D test data
X_AXIS = np.loadtxt('colofill-xdata.txt')
Y_AXIS = np.loadtxt('colofill-ydata.txt')
Z_VALUES = np.loadtxt('colofill-zdata.txt')

# ------------------------------------------------------------------------------
class MainWindow(QMainWindow, Ui_MainWindow):

    _image_canvas = None
    _miniplot_canvas = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Miniplot Prototype')

        self._create_image(X_AXIS, Y_AXIS, Z_VALUES)
        self._create_miniplot(0.5*(X_AXIS[1:] + X_AXIS[:-1]), Z_VALUES[0])

        # Add to layouts
        self.outer_layout.addWidget(self._miniplot_canvas)
        self.outer_layout.addWidget(self._image_canvas)

    def _create_image(self, x, y, z):
        fig = Figure()
        axes = fig.add_subplot(111)
        cax = axes.pcolormesh(x, y, z, cmap='viridis')
        fig.colorbar(cax)
        self._image_canvas = FigureCanvas(fig)
        self._image_canvas.draw()
        return fig

    def _create_miniplot(self, x, signal):
        fig = Figure()
        axes = fig.add_subplot(111)
        axes.plot(x, signal)
        self._miniplot_canvas = FigureCanvas(fig)
        self._miniplot_canvas.draw()
        return fig

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    qapp = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    sys.exit(qapp.exec_())
