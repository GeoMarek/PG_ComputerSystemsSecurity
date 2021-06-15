"""
Module with gui class using to get password from user
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QGroupBox, \
    QFormLayout, QLabel, QLineEdit

from src.logic.utils.hash_functions import get_hash_from
from src.logic.utils.path import init_config, init_style
from src.logic.utils.py_qt import msg_warning


class PasswordInput(QDialog):
    """
    gui for get password from user
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = init_config()
        self.setStyleSheet(init_style())
        self.__private_key: bytes = bytes()

        self.label = QLabel()
        self.label.setAlignment(QtCore.Qt.AlignVCenter)
        self.label.setText("Type password used to\nhash your private key")
        self.password = QLineEdit()

        self.form_group_box = QGroupBox("Type your password")
        layout = QFormLayout()
        layout.addRow(QLabel("Password:"), self.password)
        self.password.setText("")
        self.form_group_box.setLayout(layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Save)
        self.button_box.button(QDialogButtonBox.Save).setText("Enter")
        self.button_box.accepted.connect(self._decryption_magic)
        self.button_box.rejected.connect(self.reject)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(self.button_box)
        self.setLayout(main_layout)
        self.setWindowTitle("Asymmetric key generation")

    def _decryption_magic(self) -> None:
        """
        Method which call class to decrypt private key
        """
        _text = self.password.text()
        if len(_text) == 0:
            msg_warning("You need to type some password!", title="Empty password field")
            return None
        _hash = get_hash_from(self.password.text())
        print(_hash)
        # TODO: FEATURE rozszyfrowujemy private key i hash będzie kluczem
        # self.__private_key = odszyfruj(zaszyfrowany_private_key, hash)
        self.done(0)

    def get_key_bytes(self) -> bytes:
        """
        Get private key
        """
        return self.__private_key
