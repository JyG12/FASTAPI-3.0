from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path

BASE_DIR= Path(__file__).resolve().parent

mail_config = ConnectionConfig(
    MAIL_USERNAME = Config.MAIL_USERNAME, #"username", but we dw hardcoded so change to Config.MAIL_Username
    MAIL_PASSWORD= Config.MAIL_PASSWORD,
    MAIL_FROM= Config.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR, 'templates')
    # TEMPLATE_FOLDER=Path(BASE_DIR, "templates"),
    #some of the above are going to be read from envt variables, so need to move it there at config.py
)    

mail = FastMail(   #taking in our config
        config=mail_config
)

def create_message(recipients:list[str],subject:str,body:str):
    
    
    message = MessageSchema(recipients=recipients, subject=subject, body=body, subtype=MessageType.html)
    
    return message
