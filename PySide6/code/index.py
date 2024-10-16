from PySide6.QtWidgets import (QApplication, QMainWindow)
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtGui import QMovie
from src.window_testes import Ui_MainWindow
import time
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.movie = QMovie("code/src/imgs/Loading_2.gif")
        self.label.setMovie(self.movie)

        self.pushButton.clicked.connect(
            lambda: self.hard_work())

        self.pushButton.clicked.connect(
            lambda: self.loading())

    def loading(self):
        self._loader = Loader()
        self._thread2 = QThread()
        loader = self._loader
        thread2 = self._thread2

        #Coloca o método dentro da thread
        loader.moveToThread(thread2)
        #Quando a QThread é iniciada (started), executa método automáticamente.
        thread2.started.connect(loader.main)
        #Interrompe o loop de eventos da thread2
        loader.fim.connect(thread2.quit)
        #Remove o loader e a thread2 da memória assim que o finished ocorre
        loader.fim.connect(thread2.deleteLater)
        thread2.finished.connect(loader.deleteLater)
        #Recebe o sinal para interagir com os widget
        loader.inicio.connect(self.load) 
        loader.fim.connect(self.load) 
        #######################################
        thread2.start() 

    def load(self, value):
        if value == True:
            self.label.show()
            self.movie.start()
        elif value == False:
            self.movie.stop()
            self.label.hide()

    def hard_work(self):
        self._worker = Worker()
        self._thread = QThread()
        # Garante que o widget vai ter uma referência para worker e thread
        worker = self._worker
        thread = self._thread

        #Coloca o método dentro da thread
        worker.moveToThread(thread)
        #Inicia o "started" assim que o run começa
        thread.started.connect(worker.run)
        #Interrompe o loop de eventos da thread
        worker.finished.connect(thread.quit)
        #Remove o worker e a thread da memória assim que o finished ocorre
        worker.finished.connect(thread.deleteLater)
        thread.finished.connect(worker.deleteLater)
        #Altera um widget com base o valor de um sinal
        worker.started.connect(self.start) 
        worker.processed.connect(self.progress) 
        worker.finished.connect(self.finish) 
        #######################################
        thread.start()  
        
    def start(self, value):
        self.pushButton.setDisabled(True)
        self.progressBar.setValue(value)

    def progress(self, value):
        self.progressBar.setValue(value)

    def finish(self, value):
        self.pushButton.setDisabled(False)
        self.progressBar.setValue(value)

class Loader(QObject):
    inicio = Signal(bool)
    fim = Signal(bool)

    def main(self):
        self.run()
        self.run2()
        self.run3()

    def run(self):
        self.inicio.emit(True)
    def run2(self):
        time.sleep(5)
    def run3(self):
        self.fim.emit(False)

class Worker(QObject):
    started = Signal(int)
    processed = Signal(int)
    finished = Signal(int)

    def run(self):
        self.started.emit(0)
        for i in range(10,100, 10):
            self.processed.emit(i)
            time.sleep(0.5)
        self.finished.emit(100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = MainWindow()
    janela.show()
    app.exec()