try:
    import requests
except:
    from os import system
    system("pip install requests")
    import requests

from .methods import *


def send_fb(name, topic, body, email):
    print("ASDASDASD")
    msg = f"*Обратная связь от {name}:\n\n{topic}*\n{body}\n\nE-Mail: {email}"
    print(name)
    sendMsg(msg)