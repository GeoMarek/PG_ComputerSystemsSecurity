import sys
from src.gui.window import Window
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
