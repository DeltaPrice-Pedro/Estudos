from pathlib import Path
from os import  getenv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / 'env' / '.env')

class DeltaMail:
    def __init__(self, companie: str, recipients: list[str], content: str):
        self.sender = getenv('SENDER_EMAIL')
        self.recipients = recipients

        self.msg = MIMEMultipart('mixed')
        self.msg['Subject'] = f'{companie} - PENDÊNCIAS CONTÁBEIS'
        self.msg['From'] =  f'{self.sender} Deltaprice'
        self.msg['To'] = ', '.join(self.recipients)

        self.recipients.append(self.sender)
        self.msg.attach(MIMEText(content, 'html', 'utf-8'))
        
    def attach(self, assign: Path):
        with open(assign, 'rb') as fp:
            image_data = fp.read()

        image = MIMEImage(image_data)
        image.add_header('Content-ID', assign.stem)
        image.add_header('Content-Disposition', 'inline', filename='Assign')
        self.msg.attach(image)

    def send(self):
        server = getenv("SMTP_SERVER","")
        port = getenv("SMTP_PORT", 0)

        smtp_username = getenv("EMAIL_SENDER","")
        smtp_password = getenv("PASSWRD_SENDER","")

        with smtplib.SMTP(server, port) as smtp_server:
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.ehlo()

            smtp_server.login(smtp_username, smtp_password)
            smtp_server.sendmail(self.sender, self.recipients, self.msg.as_string())