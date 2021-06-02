"""
Module with gui class using to send files
"""

import os

from PyQt5.QtWidgets import QDialog, QComboBox, QDialogButtonBox, QVBoxLayout, QGroupBox, \
    QFormLayout, QLabel, QLineEdit, QPushButton, QFileDialog

from src.utils.path import init_config, init_style
from src.utils.py_qt import msg_success, msg_warning


class FileSenderDialog(QDialog):
    """
    gui for send files
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = init_config()
        self.setStyleSheet(init_style())
        self.path = ""
        self.form_group_box = QGroupBox("Sending files")
        self.algorithm_combobox = QComboBox()
        algorithms = self.config_file.get("algorithms").get("symmetric")
        self.algorithm_combobox.addItems(algorithms)
        self.file_button = QPushButton("Select file")
        self.file_button.clicked.connect(self._select_file_clicked)
        self.filename = QLineEdit()
        layout = QFormLayout()
        layout.addRow(QLabel("Algorithm:"), self.algorithm_combobox)
        layout.addRow(self.file_button, self.filename)
        self.form_group_box.setLayout(layout)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save)
        self.button_box.button(QDialogButtonBox.Save).setText("Send")
        self.button_box.accepted.connect(self._send_message)
        self.button_box.rejected.connect(self.reject)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(self.button_box)
        self.setLayout(main_layout)

    def _select_file_clicked(self) -> None:
        """
        Method to update forms after selecting file
        """
        self.path = QFileDialog.getOpenFileName()[0]
        self.filename.setText(os.path.basename(self.path))

    def _send_message(self) -> None:
        """
        Method which call class to send message and print it in chat
        """
        text = self.path
        mode = self.algorithm_combobox.currentText()
        if len(text) < 1:
            msg_warning("You did not select a file")
            return None
        msg_success(f"Send {text} in {mode}")
        self.filename.setText("")
        self.path = ""
        # call file sender
        # call chat printer
        return None
