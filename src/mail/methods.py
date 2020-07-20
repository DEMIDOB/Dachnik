import smtplib

from .safe_data import *

def sendMail(subject: str, body: str, to: str):
    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}\n\nАдминистрация магазина \"Дачник\"'.format(email,
                                                           to,
                                                           subject,
                                                           body)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(email, password)
    server.auth_plain()
    server.sendmail("Dachnik", to, message.encode('utf-8'))
    server.quit()
