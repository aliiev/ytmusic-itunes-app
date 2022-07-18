from PyQt5.QtCore import QObject, QThread, pyqtSignal
from yt_dlp import YoutubeDL

class Downloader(QObject):
    finished = pyqtSignal()
    ready_file = pyqtSignal(str)
    progress = pyqtSignal(float)
    speed = pyqtSignal(str)

    def __init__(self, url, parent=None):
        QThread.__init__(self, parent)
        self.url = url

    def progressHook(self, d):
        if (d['status'] == 'finished'):
            self.ready_file.emit(d['info_dict']['title'])

        if (d['status'] == 'downloading'):
            percent_str = d['_percent_str']
            percent = percent_str[percent_str.find('m') + 1:percent_str.find('%')].strip()
            
            speed_str = d['_speed_str']
            speed = speed_str[speed_str.find('m') + 1:speed_str.find('s') + 1].strip()

            self.progress.emit(float(percent))
            self.speed.emit(speed)

    def run(self):
        options = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': '/downloads/%(title)s.%(ext)s',
            'writethumbnail': 'true',
            'progress_hooks': [self.progressHook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }, {
                'key': 'FFmpegMetadata'
            }, {
                'key': 'EmbedThumbnail'
            }]
        }

        with YoutubeDL(options) as ydl:
            ydl.download([self.url])

        self.finished.emit()