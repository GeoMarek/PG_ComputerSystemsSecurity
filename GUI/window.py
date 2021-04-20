import json
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
import os

from GUI.RSAKeyGeneratorDialog import RsaKeyGeneratorDialog
from GUI.AESKeyGeneratorDialog import AesKeyGeneratorDialog
from Utils.Path import init_config, init_style


class Window(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.configFile = init_config()
        self.setStyleSheet(init_style())
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

    def _setConfig(self):
        with open(os.path.join(os.getcwd(), "config.json")) as file:
            self.configFile = json.load(file)

    def _configWindow(self):
        title = self.configFile["GUI"]["title"]
        width = self.configFile["GUI"]["width"]
        height = self.configFile["GUI"]["height"]
        self.setWindowTitle(title)
        self.setFixedSize(width, height)
