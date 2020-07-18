import requests

def sendMsg(msg):
    requests.get(f"https://api.telegram.org/bot1225466990:AAHeSxZ66mt1sOD_0ojhUf4EpbxoVK06TAY/sendMessage?chat_id=@dchadm&parse_mode=markdown&text={msg}")