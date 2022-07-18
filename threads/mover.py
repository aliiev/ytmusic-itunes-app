from PyQt5.QtCore import QObject, QDir, QThread, pyqtSignal
import os, shutil

class Mover(QObject):
    finished = pyqtSignal()

    def __init__(self, path, parent=None):
        QThread.__init__(self, parent)
        self.path = path

    def run(self):
        source_dir = QDir().currentPath() + "\\downloads"
        target_dir = self.path

        files = os.listdir(source_dir)

        for file in files:
            shutil.copy(os.path.join(source_dir, file), os.path.join(target_dir, file))
        
        self.finished.emit()