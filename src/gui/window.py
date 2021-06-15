"""
Module representing app main window
"""

import os

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from src.gui.connect_dialog import ConnectDialog
from src.gui.listener_dialog import ListenerDialog
from src.gui.message_sender_dialog import MessageSenderDialog
from src.gui.file_sender_dialog import FileSenderDialog
from src.gui.password_input import PasswordInput
from src.gui.rsa_key_generator_dialog import RsaKeyGeneratorDialog
from src.logic.utils.path import init_config, init_style


class Window(QMainWindow):
    """
    main app window
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = init_config()
        self.setStyleSheet(init_style())
        self.setWindowTitle(self.config_file.get("GUI").get("title"))

        # rsa key generator
        self._handle_rsa_storing()

        # type user friendly password
        password_input = PasswordInput()
        password_input.exec_()
        private_key_bytes = password_input.get_key_bytes()

        # connect with someone
        connect_dialog = ConnectDialog()
        connect_dialog.exec_()

        # init all widgets
        listener_dialog = ListenerDialog(connect_dialog.get_host_adress(), socket=connect_dialog.end_point)
        message_sender = MessageSenderDialog(chat=listener_dialog, socket=connect_dialog.end_point)
        file_sender = FileSenderDialog(chat=listener_dialog, socket=connect_dialog.end_point)

        # put widgets in window
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(message_sender)
        vbox.addWidget(file_sender)
        hbox.addLayout(vbox)
        hbox.addWidget(listener_dialog)
        central = QWidget()
        central.setLayout(hbox)
        self.setCentralWidget(central)

    def _is_rsa_directory_exist(self) -> bool:
        """
        Return True if exists directory, which is specified in 'config.json', else return False
        """
        return os.path.exists(os.path.join(
            os.getcwd(),
            self.config_file.get("directory").get("main_dir"),
            self.config_file.get("directory").get("asym_dir")
        ))

    def _handle_rsa_storing(self) -> None:
        """
        Handle storing rsa keys. If dir with them not exists, create new and store there
        new generated keys
        """
        if not self._is_rsa_directory_exist():
            rsa = RsaKeyGeneratorDialog()
            rsa.exec_()
