from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QComboBox, QDialogButtonBox, QVBoxLayout, QGroupBox, QFormLayout, \
    QLabel
from Encoding.RSAKeyGenerator import RsaKeyGenerator
from Utils.PyQt import msg_created_keys
from Utils.Path import init_config, init_style


class RsaKeyGeneratorDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configFile = init_config()
        self.setStyleSheet(init_style())

        self.label = QLabel()
        self.label.setText("You do not have a public key and a \n"
                           "private key in the designated directory.\n"
                           "To generate them choose an algorithm \n"
                           "and then click 'Generate key'")
        self.label.setAlignment(QtCore.Qt.AlignVCenter)

        self.algorithm_combobox = QComboBox()
        algorithms = self.configFile.get("algorithms").get("asymmetric")
        self.algorithm_combobox.addItems(algorithms)

        self._createGroupFormBox()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save)
        self.button_box.button(QDialogButtonBox.Save).setText("Generate key")
        self.button_box.accepted.connect(self._saveKeys)
        self.button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.formGroupBox)
        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)
        self.setWindowTitle("Asymmetric key generation")

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
        self.done(0)

    def reject(self):
        """To avoid closing on esc press"""
        pass
