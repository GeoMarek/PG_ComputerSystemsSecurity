"""
Module with gui class of progress bar
"""
import time

from PyQt5.QtWidgets import QDialog, QProgressBar, qApp


class ProgressBarDialog(QDialog):
    """
    Progress bar dialog
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sending file")
        self.progress = QProgressBar(self)
        self.progress.setGeometry(15, 15, 300, 25)
        self.progress.setMaximum(100)
        self.show()
        qApp.processEvents()
        self.updateProgress()
        self.close()

    def updateProgress(self) -> None:
        """
        Method to update progress bar
        """
        count = 0
        while count < 100:
            count += 1
            time.sleep(0.1)
            self.progress.setValue(count)
