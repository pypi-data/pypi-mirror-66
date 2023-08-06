#import inkex
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel

def open_gui():
    app = QApplication([])

    label = QLabel('Hello World!')

    label.show()

    app.exec_()