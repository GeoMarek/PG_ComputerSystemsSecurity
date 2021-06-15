"""
Module with gui to generate RSA keys
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QComboBox, QDialogButtonBox, QVBoxLayout, QGroupBox, \
    QFormLayout, QLabel, QLineEdit
from src.logic.key_generators.rsa_key_generator import RsaKeyGenerator
from src.logic.utils.hash_functions import get_hash_from
from src.logic.utils.py_qt import msg_success, msg_warning
from src.logic.utils.path import init_config, init_style


class RsaKeyGeneratorDialog(QDialog):
    """
    gui for generating RSA Keys
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = init_config()
        self.setStyleSheet(init_style())

        self.label = QLabel()
        self.label.setText("You do not have a public key and a \n"
                           "private key in the designated directory.\n"
                           "To generate them choose an algorithm \n"
                           "and then click 'Generate key'")
        self.label.setAlignment(QtCore.Qt.AlignVCenter)

        self.algorithm_combobox = QComboBox()
        self.algorithm_combobox.addItems(self.config.get("algorithms").get("asymmetric"))
        self.password = QLineEdit()

        self.form_group_box = QGroupBox("Creating asymmetric key")
        layout = QFormLayout()
        layout.addRow(QLabel("Algorithm:"), self.algorithm_combobox)
        layout.addRow(QLabel("Password:"), self.password)
        self.form_group_box.setLayout(layout)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save)
        self.button_box.button(QDialogButtonBox.Save).setText("Generate key")
        self.button_box.accepted.connect(self._save_keys)
        self.button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)
        self.setWindowTitle("Asymmetric key generation")

    def _save_keys(self) -> None:
        """
        Method which call class, to generate and store RSA keys
        """
        if len(self.password.text()) < 1:
            msg_warning("Password is empty")
            return None
        _hash = get_hash_from(self.password.text())
        print(_hash)
        # TODO: FEATURE szyfrujemy private key i hash będzie kluczem
        # save_keys() zapisuje klucze jawnie, prywatny trzeba zaszyfrować
        dirname = RsaKeyGenerator(self.algorithm_combobox.currentText()).save_keys()
        msg_success(f"Created keys in {dirname}", title="RSA key generation")
        self.done(0)
