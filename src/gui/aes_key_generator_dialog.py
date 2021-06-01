"""
Module with gui to generate RSA keys
"""

from PyQt5.QtWidgets import QDialog, QComboBox, QDialogButtonBox, QVBoxLayout, QGroupBox, \
    QFormLayout, QLabel
from src.key_generators.aes_key_generators import AesKeyGenerator
from src.utils.path import init_config
from src.utils.py_qt import msg_success


class AesKeyGeneratorDialog(QDialog):
    """
    gui for generating AES Keys
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = init_config()
        self.algorithm_combobox = QComboBox()
        algorithms = self.config_file.get("algorithms").get("symmetric")
        self.algorithm_combobox.addItems(algorithms)
        self._create_group_form_box()
        button_box = QDialogButtonBox(QDialogButtonBox.Save)
        button_box.button(QDialogButtonBox.Save).setText("Generate key")
        button_box.accepted.connect(self._save_keys)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)
        self.setWindowTitle("Symmetric key generation")

    def _create_group_form_box(self) -> None:
        """
        Create a form box in which user can choose an algorithm
        """
        self.form_group_box = QGroupBox("Creating symmetric key")
        layout = QFormLayout()
        layout.addRow(QLabel("Algorithm:"), self.algorithm_combobox)
        self.form_group_box.setLayout(layout)

    def _save_keys(self) -> None:
        """
        Method which call class, to generate and store AES keys
        """
        algorithm = self.algorithm_combobox.currentText()
        filename = AesKeyGenerator(algorithm).save_session_key()
        msg_success(f"Created keys as {filename}")
