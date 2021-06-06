"""
Module with gui class using to show chat
"""
import threading

from PyQt5.QtWidgets import QTextEdit
from src.logic.utils.path import init_config, init_style
from src.logic.utils.connection import receive_message_by, receive_file_by


class ListenerDialog(QTextEdit):
    """
    GUI for printing chat history
    """
    HEADER = 64
    FORMAT = 'utf-8'
    BUFFER_SIZE = 8

    def __init__(self, sender: str, socket, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sender = sender
        self.socket = socket
        self.config_file = init_config()
        self.setStyleSheet(init_style())
        self._log(f"Connect with {self.sender}")
        thread_rec = threading.Thread(target=self.loop_of_recives)
        thread_rec.start()

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

    def loop_of_recives(self):
        while True:
            recive_type = self.socket.recv(self.HEADER).decode(self.FORMAT)
            if recive_type == "f":
                self.log_received_message(receive_file_by(self.socket))
            elif recive_type == "m":
                self.log_received_message(receive_message_by(self.socket))
