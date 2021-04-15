from PyQt5.QtWidgets import QFileDialog


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
