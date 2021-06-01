"""
Module with gui class using to send messages
"""

from PyQt5.QtWidgets import QDialog, QComboBox, QDialogButtonBox, QVBoxLayout, QGroupBox, \
    QFormLayout, QLabel, QLineEdit
from utils.py_qt import msg_success, msg_warning
from utils.path import init_config, init_style


class MessageSenderDialog(QDialog):
    """
    gui for send messages
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = init_config()
        self.setStyleSheet(init_style())
        self.form_group_box = QGroupBox("Sending messages")
        self.message = QLineEdit()
        self.algorithm_combobox = QComboBox()
        algorithms = self.config_file.get("algorithms").get("symmetric")
        self.algorithm_combobox.addItems(algorithms)
        layout = QFormLayout()
        layout.addRow(QLabel("Algorithm:"), self.algorithm_combobox)
        layout.addRow(QLabel("Message:"), self.message)
        self.form_group_box.setLayout(layout)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save)
        self.button_box.button(QDialogButtonBox.Save).setText("Send")
        self.button_box.accepted.connect(self._send_message)
        self.button_box.rejected.connect(self.reject)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(self.button_box)
        self.setLayout(main_layout)

    def _send_message(self) -> None:
        """
        Method which call class to send message and print it in chat
        """
        text = self.message.text()
        mode = self.algorithm_combobox.currentText()
        if len(text) < 1:
            msg_warning("Message is empty")
            return None
        msg_success(f"Send {text} in {mode}")
        self.message.setText("")
        # call message sender
        # call chat printer
        return None
