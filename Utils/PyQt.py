from PyQt5.QtWidgets import QFileDialog, QMessageBox


def existing_directory(caption):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    directory = QFileDialog.getExistingDirectory(None, caption=caption, options=options)
    return directory


def open_file(caption):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filename, _ = QFileDialog.getOpenFileName(None, caption=caption, options=options)
    return filename


def save_file(caption):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filename, _ = QFileDialog.getSaveFileName(None, caption=caption, options=options)
    return filename


def msg_created_keys(dirpath):
    msg = QMessageBox()
    msg.setWindowTitle('Keys Generation')
    msg.setText(f"Created keys in {dirpath}")
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def msg_no_filename(text):
    msg = QMessageBox()
    msg.setWindowTitle('Warning')
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def msg_connected(text):
    msg = QMessageBox()
    msg.setWindowTitle('Connect successful')
    msg.setText(f"Successfully connected to '{text}'.\nPublic keys have been exchanged")
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
