import json
import os
from Utils.PyQt import existing_directory
from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QDialogButtonBox, QVBoxLayout, QGroupBox, QFormLayout, \
    QLabel, QMessageBox
from Encoding.RSAKeyGenerator import RsaKeyGenerator


class RsaKeyGeneratorDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setConfig()

        self.filename = QLineEdit()
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
        layout.addRow(QLabel("Key filename:"), self.filename)
        layout.addRow(QLabel("Algorithm:"), self.algorithm_combobox)
        self.formGroupBox.setLayout(layout)

    def _saveKeys(self):
        if len(self.filename.text()) == 0:
            self.messageNoFileNameTyped()
            return
        dirpath = existing_directory("Choose where to save your keys")
        key_name = self.filename.text()
        algorithm = self.algorithm_combobox.currentText()
        if dirpath:
            generator = RsaKeyGenerator(dirpath, key_name, algorithm)
            generator.init_directories()
            dirpath = generator.save_keys()
            self._messageCreatedKeys(dirpath)

    def reject(self):
        """To avoid closing on esc press"""
        pass

    def _messageCreatedKeys(self, dirpath):
        msg = QMessageBox()
        msg.setWindowTitle('Keys Generation')
        msg.setText(f"Created {self.algorithm_combobox.currentText()} keys in {dirpath}")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @staticmethod
    def messageNoFileNameTyped():
        msg = QMessageBox()
        msg.setWindowTitle('Warning')
        msg.setText('Type filename first!')
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
