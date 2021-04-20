import json
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
import os

from GUI.RSAKeyGeneratorDialog import RsaKeyGeneratorDialog
from GUI.AESKeyGeneratorDialog import AesKeyGeneratorDialog


class Window(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.configFile = None
        self._setConfig()
        self._setStyle()
        self._configWindow()

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(RsaKeyGeneratorDialog())
        hbox.addWidget(AesKeyGeneratorDialog())
        vbox.addLayout(hbox)
        # TODO: here is place to add new widgets

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
