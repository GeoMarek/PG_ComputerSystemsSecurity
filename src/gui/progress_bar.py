import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QVBoxLayout, QApplication

from src.utils.path import init_style


class SendingFileThread(QThread):
    signal = pyqtSignal(int)

    def __init__(self, path: str):
        super(SendingFileThread, self).__init__()
        self.path = path

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self.signal.emit(i)


class ProgressBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(init_style())
        self.setWindowTitle('Sending file')
        self.thread = SendingFileThread()
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.resize(300, 100)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.pbar)
        self.setLayout(self.vbox)
        self.show()
        self.btnFunc()

    def btnFunc(self):
        self.thread.signal.connect(self.signal_accept)
        self.thread.start()
        # self.btn.setEnabled(False)

    def signal_accept(self, msg):
        self.pbar.setValue(int(msg))
        if self.pbar.value() == 99:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ProgressBar()
    ex.show()
    sys.exit(app.exec_())
