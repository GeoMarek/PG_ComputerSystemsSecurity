from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
import os

from GUI.ConnectDialog import ConnectDialog
from GUI.MessageSenderDialog import MessageSenderDialog
from GUI.RSAKeyGeneratorDialog import RsaKeyGeneratorDialog
from Utils.Path import init_config, init_style


class Window(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.configFile = init_config()
        self.setStyleSheet(init_style())
        self._configWindow()

        # handle RSA key generation
        if not self.hasDirectoryRSA():
            rsa = RsaKeyGeneratorDialog()
            rsa.exec_()

        # handle connection
        ConnectDialog().exec_()

        # main window config
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(MessageSenderDialog())
        hbox.addLayout(vbox)

        # TODO: here is place to add new widgets

        central = QWidget()
        central.setLayout(hbox)
        self.setCentralWidget(central)

    def _configWindow(self):
        title = self.configFile["GUI"]["title"]
        self.setWindowTitle(title)

    def hasDirectoryRSA(self):
        return os.path.exists(os.path.join(
                os.getcwd(),
                self.configFile.get("directory").get("main_dir"),
                self.configFile.get("directory").get("asym_dir")
        ))
