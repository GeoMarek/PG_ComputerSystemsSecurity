import sys

from PyQt5.QtWidgets import QWidget, QProgressBar, QVBoxLayout, QApplication, QDialog


from src.logic.threads.copy_file_thread import CopyFileThread
# TODO: change to QProgressDialog

class ProgressBarDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sending file")
        self.thread = None
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.resize(300, 100)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.pbar)
        self.setLayout(self.vbox)
        self.btnFunc()

    def btnFunc(self):
        self.thread = CopyFileThread("")
        self.thread.signal.connect(self.signal_accept)
        self.thread.start()
        self.show()
        self.thread.wait()

    def signal_accept(self, msg):
        self.pbar.setValue(int(msg))
        if self.pbar.value() == 99:
            print("koniec")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ProgressBarDialog()
    ex.show()
    sys.exit(app.exec_())
