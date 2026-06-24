from PyQt6.QtCore import QObject
from threads.m3u_loader_thread import M3ULoaderThread
from threads.quality_thread import M3U8QualityThread

class ThreadManager(QObject):
    def __init__(self):
        super().__init__()
        self.loader_thread = None
        self.quality_thread = None

    def start_loader(self, url: str, on_finished, on_error):
        self._cleanup_thread(self.loader_thread)
        self.loader_thread = M3ULoaderThread(url)
        self.loader_thread.finished.connect(on_finished)
        self.loader_thread.error.connect(on_error)
        self.loader_thread.start()

    def start_quality(self, url: str, on_finished):
        self._cleanup_thread(self.quality_thread)
        self.quality_thread = M3U8QualityThread(url)
        self.quality_thread.finished.connect(on_finished)
        self.quality_thread.start()

    def _cleanup_thread(self, thread):
        if thread and thread.isRunning():
            thread.quit()
            thread.wait(2000)
            thread.deleteLater()

    def cleanup_all(self):
        self._cleanup_thread(self.loader_thread)
        self._cleanup_thread(self.quality_thread)