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
from PIL import Image, ImageDraw, ImageFont
import sys

# Chrome Options
# https://peter.sh/experiments/chromium-command-line-switches/



def adiciona_repr(cls):
    def meu_repr(self):
        class_name = self.__class__.__name__
        class_dict = self.__dict__
        class_repr = f'{class_name}({class_dict})'
        return class_repr
    cls.__repr__ = meu_repr
    return cls

@adiciona_repr
class Time:
    def __init__(self, nome):
        self.nome = nome

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

class ECAC(Browser):
    LINK_BASE = 'https://comprot.fazenda.gov.br/comprotegov/site/index.html#ajax/processo-consulta.html'

    def __init__(self) -> None:
        super().__init__(hide=False)
        pass

    def exec(self, num_processo):
        self.browser.get(self.LINK_BASE)
        self.browser.find_element(By.ID, 'details-button').click()
        self.browser.find_element(By.ID, 'proceed-link').click()

        self.browser.find_element(By.ID, 'campo-processo').send_keys(num_processo)

        self.browser.find_element(By.CSS_SELECTOR, '#consulta-processo > div:nth-child(9) > div > input:nth-child(1)').click()

        self.browser.switch_to.frame(self.browser.find_element(By.TAG_NAME, "iframe"))
        
        sleep(5)
        self.browser.find_element(By.ID, 'anchor').click()
        sleep(100)

class TRT(Browser):
    LINK_BASE = 'https://pje-consulta.trt3.jus.br/consultaprocessual/detalhe-processo/{0}'

    def __init__(self) -> None:
        super().__init__(hide=False)
         #horizontal, vertical
        self.cord_resp = [
            [-100,-100], [0,-100], [100,-100],
            [-100,0], [0,0], [100,0],
            [-100,100], [0,100], [100,100]
        ] 

        #Horizontal, Vertical
        self.cord_img = {
            '1':(5, 0),
            '2':(110, 0),
            '3':(220, 0),
            '4':(5, 100),
            '5':(110, 100),
            '6':(220, 100),
            '7':(5, 205),
            '8':(110, 205),
            '9':(220, 205),
        }

        self.nome_img = 'oi.png'
        pass

    def exec(self, num_processo):
        process_str = ''
        ultima_posic = 0
        num_processo = num_processo.replace('.','').replace('-','')
        for posic, value in {7:'-',9:'.',13:'.',14:'.',16:'.',20:''}.items():
            process_str = process_str + num_processo[ultima_posic : posic] + value
            ultima_posic = posic

        self.browser.get(self.LINK_BASE.format(process_str))

        self.browser.find_element(By.ID, 'amzn-captcha-verify-button').click()

        sleep(10)

        #Print captcha2
        self.foto_captcha2()
        
        # sleep(1)
        #Preenche Capacha1
        # self.preencher_captcha()

        #Tirar print
        # self.foto_cordenadas()

        #O que procurar
        # self.elemento_procurado()

        sleep(5)

    def preenche_captcha2(self):
        self.browser.find_element(By.ID, 'imagemCaptcha').screenshot(self.nome_img)

    def foto_captcha2(self):
        self.browser.find_element(By.ID, 'imagemCaptcha').screenshot(self.nome_img)
        
    def elemento_procurado(self):
        return self.browser.find_element(By.CSS_SELECTOR, '#root > div > form > div:nth-child(3) > div > div:nth-child(1) > em').text

    def foto_captcha(self):
        self.browser.find_element(By.CSS_SELECTOR, '#root > div > form > div:nth-child(3) > div > div:nth-child(2) > canvas').screenshot(self.nome_img)

        font = ImageFont.truetype("C:\\Windows\\Fonts\\Verdanab.ttf", 50)

        img = Image.open(self.nome_img)
        draw = ImageDraw.Draw(img)

        for number, posic in self.ref_img.items():
            draw.text(posic, number, 'red', font=font)

        img.show()

    def preenche_captcha(self):
        el = self.browser.find_element(By.CSS_SELECTOR, '#root > div > form > div:nth-child(3) > div > div:nth-child(2) > canvas')

        action = webdriver.common.action_chains.ActionChains(self.browser)

        for var1, var2 in [[0,100], [100,100]]:
            action.move_to_element_with_offset(el, var1, var2)
            action.click()
            action.perform()

class TST(Browser):
    LINK_BASE = 'https://consultaprocessual.tst.jus.br/consultaProcessual/consultaTstNumUnica.do?consulta=Consultar&conscsjt=&numeroTst={0}&digitoTst={1}&anoTst={2}&orgaoTst={3}&tribunalTst={4}&varaTst={5}&submit=Consultar'

    def __init__(self) -> None:
        super().__init__(hide=False)
        self.cortes_string = [7, 9, 13, 14, 16, 20]
        pass

    def exec(self, num_processo):
        partes = []
        posic_passada = 0

        for posic in self.cortes_string:
            partes.append(num_processo[posic_passada : posic])
            posic_passada = posic

        self.browser.get(self.LINK_BASE.format(
            partes[0],partes[1],partes[2],partes[3],partes[4],partes[5])
        )

        linhas = self.browser.find_elements(By.CLASS_NAME, 'historicoProcesso')

        for i in linhas:
            print(i.text)
        #24/06/2024 Conclusos para voto/decisão (Gabinete da Ministra Maria Cristina Irigoyen Peduzzi)

if __name__ == '__main__':
    ECAC().exec('10680724376201892')
    # TRT().exec('00105604320205030114')
    # TST().exec('00105604320205030114')
