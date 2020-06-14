try:
    import requests
except:
    from os import system
    system("pip install requests")
    import requests


def send_fb(name, topic, body, email):
    msg = f"*Обратная связь от {name}:\n\n{topic}*\n{body}\n\nE-Mail: {email}"
    requests.get(f"https://api.telegram.org/bot1225466990:AAHeSxZ66mt1sOD_0ojhUf4EpbxoVK06TAY/sendMessage?chat_id=@dchadm&parse_mode=markdown&text={msg}")