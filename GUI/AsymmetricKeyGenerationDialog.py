import json
import os
from Utils.PyQt import existing_directory
from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QDialogButtonBox, QVBoxLayout, QGroupBox, QFormLayout, \
    QLabel, QMessageBox
from AsymmetricEncoding.RsaKeyGenerator import RsaKeyGenerator


class AsymmetricKeyGenerationDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filename = QLineEdit()
        self.algorithm_combobox = QComboBox()
        self._setConfig()
        self._createFormGroupBox()
        self.algorithm_combobox.addItems(self.configFile['algorithms']['asymmetric'])

        button_box = QDialogButtonBox(QDialogButtonBox.Save)
        button_box.button(QDialogButtonBox.Save).setText("Generate key")
        button_box.accepted.connect(self.saveKeys)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.formGroupBox)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)
        self.setWindowTitle("Asymmetric key generation")

    def saveKeys(self):
        if len(self.filename.text()) == 0:
            self.messageNoFileNameTyped()
            return
        # TODO: add generation RSA keys
        if existing_directory("Choose where to save your keys"):
            rsa_generator = RsaKeyGenerator(
                self.filename.text(),
                self.algorithm_combobox.currentText())

    def messageCreatedKeys(self):
        msg = QMessageBox()
        msg.setWindowTitle('Keys Generation')
        msg.setText('Created and saved %s keys!' % self.algorithm_combobox.currentText())
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def _createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Creating asymmetric key")
        layout = QFormLayout()
        layout.addRow(QLabel("Key filename:"), self.filename)
        layout.addRow(QLabel("Algorithm:"), self.algorithm_combobox)
        self.formGroupBox.setLayout(layout)

    def _setConfig(self):
        with open(os.path.join(os.getcwd(), "config.json")) as file:
            self.configFile = json.load(file)

    def reject(self):
        """To avoid closing on esc press"""
        pass

    @staticmethod
    def messageNoFileNameTyped():
        msg = QMessageBox()
        msg.setWindowTitle('Warning')
        msg.setText('Type filename first!')
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
