from PyQt5.QtWidgets import QDialog, QComboBox, QDialogButtonBox, QVBoxLayout, QGroupBox, QFormLayout, \
    QLabel, QLineEdit
from Utils.PyQt import msg_success, msg_warning, open_file
from Utils.Path import init_config, init_style


class MessageSenderDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configFile = init_config()
        self.setStyleSheet(init_style())

        self.formGroupBox = QGroupBox("Sending files")

        self.message = open_file("test")
        self.algorithm_combobox = QComboBox()
        algorithms = self.configFile.get("algorithms").get("symmetric")
        self.algorithm_combobox.addItems(algorithms)

        layout = QFormLayout()
        layout.addRow(QLabel("Algorithm:"), self.algorithm_combobox)
        layout.addRow(QLabel("Select file:"), self.message)
        self.formGroupBox.setLayout(layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Save)
        self.button_box.button(QDialogButtonBox.Save).setText("Send")
        self.button_box.accepted.connect(self._sendMessage)
        self.button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.formGroupBox)
        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)

    def _createGroupFormBox(self):
        self.formGroupBox = QGroupBox("Sending files")
        layout = QFormLayout()
        layout.addRow(QLabel("Algorithm:"), self.algorithm_combobox)
        layout.addRow(QLabel("Selected file:"), self.message)
        self.formGroupBox.setLayout(layout)

    def _sendMessage(self):
        text = self.message.text()
        mode = self.algorithm_combobox.currentText()
        if len(text) < 1:
            msg_warning("You did not slect a file")
            return
        else:
            msg_success(f"Send {text} in {mode}")
            self.message.setText("")
            return

    def reject(self):
        """To avoid closing on esc press"""
        pass
