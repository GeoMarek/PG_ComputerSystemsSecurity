import os

from PyQt5.QtWidgets import QDialog, QComboBox, QDialogButtonBox, QVBoxLayout, QGroupBox, QFormLayout, \
    QLabel, QLineEdit, QPushButton, QFileDialog

from Utils.Path import init_config, init_style
from Utils.PyQt import msg_success, msg_warning


class FileSenderDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configFile = init_config()
        self.setStyleSheet(init_style())

        # layout title
        self.formGroupBox = QGroupBox("Sending files")

        # choose algorithm
        self.algorithm_combobox = QComboBox()
        algorithms = self.configFile.get("algorithms").get("symmetric")
        self.algorithm_combobox.addItems(algorithms)

        # test with button
        self.file_button = QPushButton("Select file")
        self.file_button.clicked.connect(lambda: self._select_file_clicked())
        self.filename = QLineEdit()

        # set layout
        layout = QFormLayout()
        layout.addRow(QLabel("Algorithm:"), self.algorithm_combobox)
        layout.addRow(self.file_button, self.filename)
        self.formGroupBox.setLayout(layout)

        # send button
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save)
        self.button_box.button(QDialogButtonBox.Save).setText("Send")
        self.button_box.accepted.connect(self._sendMessage)
        self.button_box.rejected.connect(self.reject)

        # set main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.formGroupBox)
        main_layout.addWidget(self.button_box)
        self.setLayout(main_layout)

    def _select_file_clicked(self):
        self.path = QFileDialog.getOpenFileName()[0]
        self.filename.setText(os.path.basename(self.path))

    def _sendMessage(self):
        text = self.path
        mode = self.algorithm_combobox.currentText()
        if len(text) < 1:
            msg_warning("You did not select a file")
            return
        else:
            msg_success(f"Send {text} in {mode}")
            self.message.setText("")
            return

    def reject(self):
        """To avoid closing on esc press"""
        pass
