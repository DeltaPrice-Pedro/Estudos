from pathlib import Path
from os import  getenv

from dotenv import load_dotenv
from redmail import EmailSender
from redmail import outlook

load_dotenv(Path(__file__).parent / 'env' / '.env')

class redEmail:
    def __init__(self):
        server = getenv("SMTP_SERVER","")
        port = getenv("SMTP_PORT", 0)
        
        self.email_sender = EmailSender(host= server, port= port)
        
    def send(self, companie: str, recipients: list[str], content: str, assign_filename: Path):
        sender = getenv('SENDER_EMAIL')
        outlook.username = 'contabilidade@deltaprice.com.br'
        outlook.password = ';E/UHMPpJch&6qa'

        outlook.send(
            subject= f'{companie} - PENDÊNCIAS CONTÁBEIS',
            sender= sender,
            receivers= recipients,
            html= content,
            body_images={
                assign_filename.stem: assign_filename.__str__(),
            }
        )