from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, QSettings
from design import Ui_MainWindow
from threads.downloader import Downloader
from threads.mover import Mover
from threads.cleaner import Cleaner
import os, sys

class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)

        self.settings = QSettings('ytmusic-itunes-app', 'app')
        self.urlInput.setText(self.settings.value('youtube-url'))
        self.folderInput.setText(self.settings.value('itunes-folder'))

        self.downloadedCount() 
        self.downloadBtn.clicked.connect(self.downloadBtnClick)
        self.folderBtn.clicked.connect(self.folderBtnClick)

    def downloaderThread(self):
        self.thread = QThread()
        self.downloader = Downloader(url=self.urlInput.text())
        self.downloader.moveToThread(self.thread)

        self.thread.started.connect(self.downloader.run)
        self.downloader.finished.connect(self.thread.quit)
        self.downloader.finished.connect(self.downloader.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: self.outputTextEdit.append('Download finished.'))
        self.thread.finished.connect(self.moverThread)

        self.thread.start()
        self.outputTextEdit.append('Download started...')
        self.downloader.progress.connect(lambda percent: self.progressBar.setValue(int(percent)))
        self.downloader.speed.connect(lambda speed: self.speedLabel.setText(speed))
        self.downloader.ready_file.connect(lambda ready_file: self.outputTextEdit.append("Downloaded: " + ready_file))

    def moverThread(self):
        self.thread = QThread()
        self.mover = Mover(path=self.folderInput.text())
        self.mover.moveToThread(self.thread)

        self.thread.started.connect(self.mover.run)
        self.mover.finished.connect(self.thread.quit)
        self.mover.finished.connect(self.mover.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: self.outputTextEdit.append('Files copied successfully.'))
        self.thread.finished.connect(self.enableInputs)
        self.thread.finished.connect(self.resetProgress)

        self.thread.start()
        self.outputTextEdit.append('Copying music to iTunes folder...')

    def cleanerThread(self):
        if self.deleteCheckBox.isChecked():
            self.thread = QThread()
            self.cleaner = Cleaner()
            self.cleaner.moveToThread(self.thread)

            self.thread.started.connect(self.cleaner.run)
            self.cleaner.finished.connect(self.thread.quit)
            self.cleaner.finished.connect(self.cleaner.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(lambda: self.outputTextEdit.append('Files deleted successfully.'))
            self.thread.finished.connect(self.downloaderThread)

            self.thread.start()
            self.outputTextEdit.append('Deleting earlier downloaded files...')
        else:
            self.downloaderThread()

    def enableInputs(self, enabled=True):
        self.downloadBtn.setEnabled(enabled)
        self.folderBtn.setEnabled(enabled)
        self.urlInput.setEnabled(enabled)
        self.folderInput.setEnabled(enabled)
        self.deleteCheckBox.setEnabled(enabled)

    def resetProgress(self):
        self.progressBar.setValue(0)
        self.speedLabel.setText('0 KiB/s')

    def downloadedCount(self):
        _translate = QtCore.QCoreApplication.translate
        count = len([f for f in os.listdir('downloads') if os.path.isfile(os.path.join('downloads', f))])
        size = round(sum(d.stat().st_size for d in os.scandir('downloads') if d.is_file()) / 1024 / 1024, 1)
        self.deleteCheckBox.setText(_translate("MainWindow", "Delete earlier downloaded files ({} tracks | {} Mb)".format(count, size)))

    def downloadBtnClick(self):
        if self.urlInput.text() != '' and self.folderInput.text() != '':
            self.settings.setValue('youtube-url', self.urlInput.text())
            self.settings.setValue('itunes-folder', self.folderInput.text())
            self.enableInputs(False)
            self.cleanerThread()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText("Youtube URL or iTunes folder is empty!")
            msg.setWindowTitle("Error")
            msg.exec_()

    def folderBtnClick(self):
        defaultFolder = QtCore.QDir().homePath() + '\\Music\\'
        folder = QtWidgets.QFileDialog.getExistingDirectory(None, "Select iTunes Music folder", defaultFolder)

        if folder:
            self.folderInput.setText(str(folder))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = App()
    MainWindow.show()
    sys.exit(app.exec_())