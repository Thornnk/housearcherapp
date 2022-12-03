import json
import smtplib
from message import Message
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Notification:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def create_notif():
        # TODO Modify data here (prettify)
        with open("results.json") as j:
            message = Message(json.load(j))
            return message.content

    def get_credentials(self):
        with open('filekey.key', 'rb') as filekey:
            fernet = Fernet(filekey.read())

        with open('cred', 'rb') as enc_file:
            pwd = fernet.decrypt(enc_file.read()).decode()

        return "housearcherapp@gmail.com", pwd

    def send(self, data):
        if self.config["notifications"]:
            if data:
                creds = self.get_credentials()
                for receiver in self.config["receiver_emails"]:
                    message = MIMEMultipart("alternative")
                    message["Subject"] = "Viviendas que he encontrado"
                    message["From"] = creds[0]
                    message["To"] = receiver
                    message.attach(MIMEText(f'{data}', "html"))

                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(creds[0], creds[1])
                        server.sendmail(
                            creds[0], receiver, message.as_string()
                        )

    def run(self):
        notification = self.create_notif()
        if notification:
            self.send(notification)

# Media W/h -> 0.00030188
# Monitores (360h, 23W)     ->  5.04€
# TV (42h, 180W)            ->  2.30€
# Frigo (720h, 240W)        ->  52.16€
# Secador (32h, 1600W)      ->  15.46€
# Plancha pelo ()
