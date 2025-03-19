import json
import requests
from zipfile import ZipFile 
import shutil
import os
from pathlib import Path

class DriverMaintenance:
    URL = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
    query_parameters = {"downloadformat": "zip"}
    zip_path = Path(__file__).parent / "chomedriver.zip"
    exe_dir_path = Path(__file__).parent / 'chromedriver-win64' / 'chromedriver.exe'
    exe_path = Path(__file__).parent / 'chromedriver.exe'

    def __init__(self):
        pass

    def upgrade(self):
        try:
            self._zip()
            self._extract_move()
            print("Arquivo movido com sucesso!")
        except FileNotFoundError:
            print("O arquivo de origem não foi encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def _zip(self):
        object_json = self._download_json()
        response = self._driver_response(object_json)
        print(response.ok)
        with open(self.zip_path, mode="wb") as file:
            file.write(response.content)

    def _download_json(self):
        response = requests.get(self.URL)
        return json.loads(response.text)

    def _driver_response(self, object_json):
        latest_driver_url = object_json['channels']['Stable']\
                                ['downloads']['chromedriver'][4]['url']
        return requests.get(latest_driver_url, self.query_parameters)

    def _extract_move(self):
        with ZipFile(self.zip_path, 'r') as zObject: 
            zObject.extractall(path= Path(__file__).parent) 

        shutil.move(self.exe_dir_path, self.exe_path)

        shutil.rmtree(self.exe_dir_path.parent)
        os.remove(self.zip_path)

if __name__ == '__main__':
    dm = DriverMaintenance()
    dm.upgrade()