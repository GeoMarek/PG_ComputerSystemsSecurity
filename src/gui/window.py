"""
Module representing app main window
"""

import os

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from src.gui.connect_dialog import ConnectDialog
from src.gui.listener_dialog import ListenerDialog
from src.gui.message_sender_dialog import MessageSenderDialog
from src.gui.file_sender_dialog import FileSenderDialog
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
        self._handle_rsa_storing()

        # init all widgets
        connection_dialog = ConnectDialog()
        connection_dialog.exec_()
        chat_printer = ListenerDialog(connection_dialog.get_host_adress())
        message_sender = MessageSenderDialog(chat=chat_printer)
        file_sender = FileSenderDialog(chat=chat_printer)

        # put widgets in window
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(message_sender)
        vbox.addWidget(file_sender)
        hbox.addLayout(vbox)
        hbox.addWidget(chat_printer)
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
