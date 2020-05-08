# we import the Twilio client from the dependency we just installed
from twilio.rest import Client
import config as cfg

class SendSMS:
    
    @staticmethod
    def send_sms(text_message):
        client = Client(cfg.ACCOUNT_SID, cfg.AUTH_TOKEN)

        client.messages.create(to=cfg.TO_NUM, 
                            from_=cfg.FROM_NUM, 
                            body=text_message)
