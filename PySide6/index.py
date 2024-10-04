from PySide6.QtWidgets import (QApplication, QMainWindow)
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtGui import QIcon
from window import Ui_MainWindow
import time
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowIcon((QIcon('cps logo.png')))

        self.radioButton.clicked.connect(
            lambda: self.set_nivel())

    def hard_work(self):
        self._worker = Worker()
        self._thread = QThread()
        worker = self._worker
        thread = self._thread

        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        #######################################
        worker.finished.connect(quit)
        worker.finished.connect(thread.deleteLater)
        thread.finished.connect(worker.deleteLater)
        #######################################
        worker.processed.connect( 
            lambda value: self.progressBar.setValue(value) ) 
        #######################################
        thread.start()  

class Worker(QObject):
    started = Signal(int)
    processed = Signal(int)
    finished = Signal(int)

    def run(self):
        self.started.emit(0)
        for i in range(10,100, 10):
            self.processed.emit(i)
            time.sleep(2)
        self.finished.emit(100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = MainWindow()
    janela.show()
    app.exec()