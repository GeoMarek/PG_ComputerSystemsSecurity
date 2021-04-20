from PyQt5.QtWidgets import QDialog, QComboBox, QDialogButtonBox, QVBoxLayout, QGroupBox, QFormLayout, \
    QLabel
from Encoding.AESKeyGenerator import AesKeyGenerator
from Utils.Path import init_config
from Utils.PyQt import msg_created_keys


class AesKeyGeneratorDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configFile = init_config()

        self.algorithm_combobox = QComboBox()
        algorithms = self.configFile.get("algorithms").get("symmetric")
        self.algorithm_combobox.addItems(algorithms)

        self._createGroupFormBox()
        button_box = QDialogButtonBox(QDialogButtonBox.Save)
        button_box.button(QDialogButtonBox.Save).setText("Generate key")
        button_box.accepted.connect(self._saveKeys)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.formGroupBox)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)
        self.setWindowTitle("Symmetric key generation")

    def _createGroupFormBox(self):
        self.formGroupBox = QGroupBox("Creating symmetric key")
        layout = QFormLayout()
        layout.addRow(QLabel("Algorithm:"), self.algorithm_combobox)
        self.formGroupBox.setLayout(layout)

    def _saveKeys(self):
        algorithm = self.algorithm_combobox.currentText()
        generator = AesKeyGenerator(algorithm)
        filename = generator.save_session_key()
        msg_created_keys(filename)

    def reject(self):
        """To avoid closing on esc press"""
        pass
