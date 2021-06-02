"""
Module with gui class using to show chat
"""
from PyQt5.QtWidgets import QTextEdit
from src.logic.utils.path import init_config, init_style


class ListenerDialog(QTextEdit):
    """
    GUI for printing chat history
    """
    def __init__(self, sender: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sender = sender
        self.config_file = init_config()
        self.setStyleSheet(init_style())
        self._log(f"Connect with {self.sender}")

    def _log(self, message: str) -> None:
        """
        Print message in chat
        """
        self.append(message)

    def log_sent_message(self, message: str) -> None:
        """
        Print sent message in chat
        """
        self._log(f"Me: {message}")

    def log_received_message(self, message: str) -> None:
        """
        Print received message in chat
        """
        self._log(f"{self.sender}: {message}")
