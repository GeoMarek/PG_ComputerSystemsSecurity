"""
Module with gui class using to connect with someone
"""
import socket
import threading

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QGroupBox, \
    QFormLayout, QLabel, QLineEdit

from src.utils.connection import handle_connection
from src.logic.utils.path import init_config, init_style
from src.logic.utils.py_qt import msg_warning, msg_success


class ConnectDialog(QDialog):
    """
    gui for connect with someone
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = init_config()
        self.setStyleSheet(init_style())
        self.host_addres = None
        self.label = QLabel()
        self.label.setAlignment(QtCore.Qt.AlignVCenter)
        self.label.setText("To send messages and file to \n"
                           "your friend, you need to set\n"
                           "connection to your friend ")
        self.filename = QLineEdit()
        self._create_group_form_box()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save)
        self.button_box.button(QDialogButtonBox.Save).setText("Connect")
        self.button_box.accepted.connect(self._connect)
        self.button_box.rejected.connect(self.reject)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(self.button_box)
        self.setLayout(main_layout)
        self.setWindowTitle("Asymmetric key generation")

    def _create_group_form_box(self) -> None:
        """
        Init form with address
        """
        self.form_group_box = QGroupBox("Configure connection")
        layout = QFormLayout()
        layout.addRow(QLabel("Address:"), self.filename)
        self.form_group_box.setLayout(layout)

    def _connect(self) -> None:
        """
        Method which call class to connect with someone
        """
        address = self.filename.text()
        # add some method to validate address, for good now addres is 'ok'
        if len(address) == 0:
            msg_warning("You need to specify address", title="Empty address field")
            return None
        address_tuple = (address, 5050)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # robimy socketa
        result_of_check = s.connect_ex(address_tuple)  # sprawdzamy czy możemy się połączyć z podanym addresem
        if result_of_check == 0:  # udało sie połączyć
            print("Port is open so we connected")
            handle_connection(s)
            msg_success(f"Successful connect to '{address}'", title="Connected")
            self.done(0)
            return None
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Port is not open; lets create server")
            s.bind(address_tuple)
            s.listen()
            # TODO: poprawic czekanie na polaczenie, zeby sie nie wieszalo okno
            s2, not_my_addr = s.accept()
            thread = threading.Thread(target=handle_connection, args=(s2,))
            thread.start()
            msg_success(f"Someone connected to me", title="Connected")
            self.done(0)
            return None

    def get_host_adress(self) -> str:
        """
        Get address you were connected to
        """
        return self.host_addres
