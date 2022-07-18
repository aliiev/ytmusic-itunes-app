from PyQt5.QtCore import QObject, QThread, pyqtSignal
import os, shutil

class Cleaner(QObject):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        for filename in os.listdir('downloads'):
            file_path = os.path.join('downloads', filename)

            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        
        self.finished.emit()