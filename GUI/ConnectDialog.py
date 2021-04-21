from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QGroupBox, QFormLayout, \
    QLabel, QLineEdit
from Utils.Path import init_config, init_style
from Utils.PyQt import msg_warning, msg_success


class ConnectDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configFile = init_config()
        self.setStyleSheet(init_style())

        self.label = QLabel()
        self.label.setAlignment(QtCore.Qt.AlignVCenter)
        self.label.setText("To send messages and file to \n"
                           "your friend, you need to set\n"
                           "connection to your friend ")

        self.filename = QLineEdit()
        self._createGroupFormBox()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save)
        self.button_box.button(QDialogButtonBox.Save).setText("Connect")
        self.button_box.accepted.connect(self._connect)
        self.button_box.rejected.connect(self.reject)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.formGroupBox)
        main_layout.addWidget(self.button_box)
        self.setLayout(main_layout)
        self.setWindowTitle("Asymmetric key generation")

    def _createGroupFormBox(self):
        self.formGroupBox = QGroupBox("Configure connection")
        layout = QFormLayout()
        layout.addRow(QLabel("Address:"), self.filename)
        self.formGroupBox.setLayout(layout)

    def _connect(self):
        address = self.filename.text()
        if len(address) == 0:
            msg_warning("You need to specify address", title="Empty address field")
            return
        elif address in ["ok", "Ok", "OK"]:
            msg_success(f"Successful connect to '{address}'", title="Connected")
            self.done(0)
        else:
            msg_warning("Something went wrong. Try again.")
            return

    def reject(self):
        """To avoid closing on esc press"""
        pass
