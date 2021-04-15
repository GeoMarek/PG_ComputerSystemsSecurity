import json
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QDialog
import os

from GUI.AsymmetricKeyGenerationDialog import AsymmetricKeyGenerationDialog


class Window(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.configFile = None
        self._setConfig()
        self._setStyle()
        self._configWindow()

        vbox = QVBoxLayout()
        vbox.addWidget(AsymmetricKeyGenerationDialog())
        # TODO: what boxes need to add

        central = QWidget()
        central.setLayout(vbox)
        self.setCentralWidget(central)

    def _setStyle(self):
        with open(os.path.join(os.getcwd(), "GUI", "style.css")) as styles:
            self.setStyleSheet(styles.read())

    def _setConfig(self):
        with open(os.path.join(os.getcwd(), "config.json")) as file:
            self.configFile = json.load(file)

    def _configWindow(self):
        title = self.configFile["GUI"]["title"]
        width = self.configFile["GUI"]["width"]
        height = self.configFile["GUI"]["height"]
        self.setWindowTitle(title)
        self.setFixedSize(width, height)
