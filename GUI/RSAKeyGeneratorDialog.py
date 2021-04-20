import json
import os
from PyQt5.QtWidgets import QDialog, QComboBox, QDialogButtonBox, QVBoxLayout, QGroupBox, QFormLayout, \
    QLabel
from Encoding.RSAKeyGenerator import RsaKeyGenerator
from Utils.PyQt import msg_created_keys


class RsaKeyGeneratorDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setConfig()

        self.algorithm_combobox = QComboBox()
        algorithms = self.configFile.get("algorithms").get("asymmetric")
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
        self.setWindowTitle("Asymmetric key generation")

    def _setConfig(self):
        with open(os.path.join(os.getcwd(), "config.json")) as file:
            self.configFile = json.load(file)

    def _createGroupFormBox(self):
        self.formGroupBox = QGroupBox("Creating asymmetric key")
        layout = QFormLayout()
        layout.addRow(QLabel("Algorithm:"), self.algorithm_combobox)
        self.formGroupBox.setLayout(layout)

    def _saveKeys(self):
        algorithm = self.algorithm_combobox.currentText()
        generator = RsaKeyGenerator(algorithm)
        dirname = generator.save_keys()
        msg_created_keys(dirname)

    def reject(self):
        """To avoid closing on esc press"""
        pass
