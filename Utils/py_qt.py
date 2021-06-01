"""
A collection of useful simple PyQt functions
"""

from PyQt5.QtWidgets import QMessageBox


def msg_success(text: str, title: str = "Successful") -> None:
    """
    Show successfulmessage box
    :param text: content of message
    :param title: name of message
    """
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def msg_warning(text: str, title: str = "Warning") -> None:
    """
    Show message box with warning
    :param text: content of warning
    :param title: name of warning
    """
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
