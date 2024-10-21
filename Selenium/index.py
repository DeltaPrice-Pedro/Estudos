from pathlib import Path
from time import sleep
import keyboard
from abc import abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from PIL import Image
import sys

from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout,QPushButton, QLineEdit
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QThread, QObject, Signal
from window_selenium import Ui_MainWindow

# Chrome Options
# https://peter.sh/experiments/chromium-command-line-switches/

class Browser:
    ROOT_FOLDER = Path(__file__).parent
    CHROME_DRIVER_PATH = ROOT_FOLDER / 'drivers' / 'chromedriver.exe'

    def __init__(self, options = (), hide = True) -> None:
        self.browser = self.make_chrome_browser(*options)
        if hide == True:
            self.browser.set_window_position(-10000,0)
            
        pass

    def make_chrome_browser(self,*options: str) -> webdriver.Chrome:
        chrome_options = webdriver.ChromeOptions()

        # chrome_options.add_argument('--headless')
        if options is not None:
            for option in options:
                chrome_options.add_argument(option)

        chrome_service = Service(
            executable_path=str(self.CHROME_DRIVER_PATH),
        )

        browser = webdriver.Chrome(
            service=chrome_service,
            options=chrome_options
        )

        return browser

class janelaCaptcha(QWidget):
    def __init__(self, nome_img):
        super().__init__()
        Image.open(nome_img).crop([300, 430, 430, 480]).save(nome_img)
        self.label.setPixmap(QPixmap(nome_img))

        layout = QVBoxLayout()

        self.label = QLabel()
        self.text_input = QLabel('Favor insira a sequência a seguir')
        self.input = QLineEdit()
        self.input.setMaxLength(4)

        layout.addWidget(self.label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.input)

        self.setLayout(layout)

    def tentar_combinacao(self):      
        return self.input.text()

class Worker(QObject):
    inicio = Signal(str)
    valor = Signal(str)
    fim = Signal(str)

    def executar_janela(self):
        self.janela = janelaCaptcha('image.png')
        self.janela.show()
        valor_janela = ''
        while len(valor_janela) != 4:
            valor_janela = self.janela.tentar_combinacao()
            self.valor.emit(valor_janela)


class EPROC(Browser):
    LINK_BASE = 'https://eproc1g.trf6.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica'
    INPUT = 'txtNumProcesso'
    CAPTCHA = 'txtInfraCaptcha'
    CONTULTAR = 'sbmNovo'
    TABLE_CONTENT = '#divInfraAreaProcesso > table > tbody'
    TIME_TO_WAIT = 1
    WAIT_CAPTCHA = 2
    FRAME_PRINT = [300, 430, 430, 480]

    def __init__(self) -> None:
        super().__init__(hide=False)
        pass

    def exec(self, num_process):
        self.browser.get(self.LINK_BASE)
        self.browser.find_element(By.ID, self.INPUT).send_keys(num_process)
        self.tentar_consulta()
        #return self.__valor_janela()

    def tentar_consulta(self):
        self.browser.find_element(By.ID, self.CONTULTAR).click()
        keyboard.press_and_release('enter')
        sleep(self.TIME_TO_WAIT)
        try:
            #se o captcha aparece, esperar para preenchê-lo
            if self.browser.find_element(By.ID, self.CAPTCHA).is_displayed():
                return self.preencher_captcha()
        except:
            return None

    def preencher_captcha(self):
        self.browser.save_screenshot("image.png")
        self.hard_work()

        while len(self.valor_janela) != 4:
            sleep(self.WAIT_CAPTCHA)

        self.browser.find_element(By.ID, 'txtInfraCaptcha')\
            .text(self.valor_janela)
        self.tentar_consulta()

        return None

    def hard_work(self):
        self._worker = Worker()
        self._thread = QThread()
        # Garante que o widget vai ter uma referência para worker e thread
        worker = self._worker
        thread = self._thread

        worker.moveToThread(thread)
        thread.started.connect(worker.executar_janela)
        worker.finished.connect(thread.quit)
        worker.finished.connect(thread.deleteLater)
        thread.finished.connect(worker.deleteLater)
        worker.valor.connect(self.progress) 
        #######################################
        thread.start()  

    def progress(self, valor):
        self.valor_janela = valor

    def __conteudo(self):
        tbody = self.browser.find_element(By.CSS_SELECTOR, self.TABLE_CONTENT)
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        rows.pop(0)
        return rows

class PJE(Browser):
    CLASS_ELEMENTS = 'col-sm-12'
    TIME_TO_WAIT = 3
    INPUT = 'fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso'
    BTN_PESQUISAR = 'fPP:searchProcessos'
    JANELA_PROCESSO = '#fPP\\:processosTable\\:632256959\\:j_id245 > a'
    TABELA_CONTEUDO = 'j_id134:processoEvento'
    LINK_BASE = 'https://pje-consulta-publica.tjmg.jus.br/'
    LINK_JANELA = 'https://pje-consulta-publica.tjmg.jus.br/pje/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca'

    def __init__(self) -> None:
        super().__init__()
        pass

    def exec(self, num_processo):
        self.browser.get(self.LINK_BASE)

        self.browser.find_element(By.NAME, self.INPUT).send_keys(num_processo)

        self.browser.find_element(By.NAME, self.BTN_PESQUISAR).click()

        sleep(self.TIME_TO_WAIT)

        metodo_janela = self.browser.find_element(By.CSS_SELECTOR, self.JANELA_PROCESSO).get_attribute('onclick')

        link_janela = metodo_janela[metodo_janela.rfind('='):]

        return {num_processo: self.__valor_janela(link_janela)}

    def __valor_janela(self, endereco: str):
        self.browser.get(self.LINK_JANELA + endereco[:len(endereco)-2])

        sleep(self.TIME_TO_WAIT)

        tbody = self.browser.find_element(By.ID, self.TABELA_CONTEUDO)
        results = tbody.find_elements(By.TAG_NAME, 'span')
        for value in results:
            print(value.text)
        return results
    
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)
        # PJE().exec('5147698-10.2023.8.13.0024')

    def show_new_window(self, checked):
        EPROC().exec('10804583320214013800')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()