"""
Module with gui to generate RSA keys
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QComboBox, QDialogButtonBox, QVBoxLayout, QGroupBox, \
    QFormLayout, QLabel
from key_generators.rsa_key_generator import RsaKeyGenerator
from utils.py_qt import msg_success
from utils.path import init_config, init_style


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
        algorithms = self.config.get("algorithms").get("asymmetric")
        self.algorithm_combobox.addItems(algorithms)

        self._create_group_form_box()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save)
        self.button_box.button(QDialogButtonBox.Save).setText("Generate key")
        self.button_box.accepted.connect(self._save_keys)
        self.button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self._form_group_box)
        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)
        self.setWindowTitle("Asymmetric key generation")

    def _create_group_form_box(self) -> None:
        """
        Create a form box in which user can choose an algorithm
        """
        self._form_group_box = QGroupBox("Creating asymmetric key")
        layout = QFormLayout()
        layout.addRow(QLabel("Algorithm:"), self.algorithm_combobox)
        self._form_group_box.setLayout(layout)

    def _save_keys(self) -> None:
        """
        Method which call class, to generate and store RSA keys
        """
        algorithm = self.algorithm_combobox.currentText()
        dirname = RsaKeyGenerator(algorithm).save_keys()
        msg_success(f"Created keys in {dirname}", title="RSA key generation")
        self.done(0)
