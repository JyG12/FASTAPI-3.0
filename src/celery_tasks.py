from celery import Celery
from src.mail import mail, create_message
from asgiref.sync import async_to_sync

c_app = Celery("my_app")
c_app.config_from_object('src.config')

import platform
if platform.system() == "Windows":
    c_app.conf.worker_pool = "solo"



@c_app.task()
def send_email(recipients:list[str], subject:str, body:str):
    message = create_message(recipients = recipients, subject = subject, body= body)
    
    async_to_sync(mail.send_message)(message)
    print("Email sent")