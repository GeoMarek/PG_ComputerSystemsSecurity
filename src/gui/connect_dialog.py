"""
Module with gui class using to connect with someone
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QGroupBox, \
    QFormLayout, QLabel, QLineEdit
from src.utils.path import init_config, init_style
from src.utils.py_qt import msg_warning, msg_success


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
        if address in ["ok", "Ok", "OK"]:
            msg_success(f"Successful connect to '{address}'", title="Connected")
            self.done(0)
            self.host_addres = "Odbiorca"
            # call connect class
            return None
        msg_warning("Something went wrong. Try again.")
        return None

    def get_host_adress(self) -> str:
        """
        Get address you were connected to
        """
        return self.host_addres
