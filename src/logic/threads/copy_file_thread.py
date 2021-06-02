"""
Module with thread class to copy files
"""

import time

from PyQt5.QtCore import QThread, pyqtSignal


class CopyFileThread(QThread):
    signal = pyqtSignal(int)

    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.05)
            print(f"teraz: {i}")
            self.signal.emit(i)
