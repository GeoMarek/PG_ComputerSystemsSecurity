from GUI.window import Window
from PyQt5.QtWidgets import QApplication
import sys

# import os
# import shutil
# stored_keys = os.path.join(os.getcwd(), "stored_data")
# if os.path.exists(stored_keys):
#     shutil.rmtree(stored_keys)

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()
