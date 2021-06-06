"""
Module with gui class of progress bar
"""
import time

from PyQt5.QtWidgets import QDialog, QProgressBar, qApp


class ProgressBarDialog(QDialog):
    """
    Progress bar dialog
    """
    def __init__(self, count: int, window_header: str = "Sending file"):
        super().__init__()
        self.setWindowTitle(window_header)
        self.progress = QProgressBar(self)
        self.progress.setGeometry(15, 15, 300, 25)
        self.progress.setMaximum(100)
        self.count = count
        self.step = 100 // self.count
        self.actual_percentage = 0
        self.show()
        qApp.processEvents()
        self.updateProgress()
        self.close()

    def one_step_forward(self) -> None:
        """
        Method to update progress bar
        """
        self.actual_percentage += self.step
        self.progress.setValue(self.actual_percentage)

    def updateProgress(self) -> None:
        """
        Method to update progress bar
        """
        count = 0
        while count < 100:
            count += 1
            time.sleep(0.1)
            self.progress.setValue(count)

    def close_if_over(self) -> None:
        """
        Close progress bar window if its done
        """
        if self.actual_percentage > 99:
            self.close()