from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Chrome Options
# https://peter.sh/experiments/chromium-command-line-switches/

class Browser:
    ROOT_FOLDER = Path(__file__).parent
    CHROME_DRIVER_PATH = ROOT_FOLDER / 'drivers' / 'chromedriver.exe'

    def __init__(self, options = '') -> None:
        self.browser = self.make_chrome_browser(*options)
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

class Tribunal:
    TIME_TO_WAIT = 10
    def __init__(self, option = '') -> None:
        self.browser = Browser(option)

        tipo = self.__apurar()
        pass


class PJE(Tribunal):
    CLASS_ELEMENTS = 'col-sm-12'

    def __init__(self, options = '') -> None:
        super().__init__('')
        self.browser.get('https://pje-consulta-publica.tjmg.jus.br/')
        pass

    def exec(self, num):
        self.browser.get(self.link)

        self.browser.find_element(By.NAME, 
            'fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso').send_keys(num)


        self.browser.find_element(By.NAME, 'fPP:searchProcessos').click()

        sleep(self.TIME_TO_WAIT)

        self.browser.find_element(By.CSS_SELECTOR,'#fPP\\:processosTable\\:632256959\\:j_id245 > a').click()


class Juiz:
    def __init__(self) -> None:
        self.processos = {}

        self.ref = {
            'pje': PJE(),
        }
        pass

    def add_processo(self, num:str, nome:str):
        self.processos[num, self.__apurar(nome)]

    def __apurar(self, nome:str):
        for key, value in self.ref.items():
            if nome == key:
                return value 
        raise Exception('Processo de tribunal não identificado')
    
    def pesquisar(self):
        for num, tribunal in self.processos.items:
            infos = tribunal.infos()
            browser = Browser(infos['options'])

            browser.get(infos['link'])
            

if __name__ == '__main__':
    ...  