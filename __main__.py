from GUI.window import Window
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
