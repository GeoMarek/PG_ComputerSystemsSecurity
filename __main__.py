from gui.window import Window
from PyQt5.QtWidgets import QApplication
import sys


app = QApplication(sys.argv)
Window().show()
app.exec_()
