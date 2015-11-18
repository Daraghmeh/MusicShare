from static import config,sendtext
from static import adminnumber
import speakermanager

adminmode = config['DEFAULT']['admin_mode'] == "true"

def clear(message, sender):
    if adminmode and sender == adminnumber:
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " + config['DEFAULT']['master_name'] + ", the system has been CLEARED.")
        speakermanager.clear()
    else:
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "You are not " + config['DEFAULT']['master_name'] + " ... Please have" + adminnumber[:-4] + "send this command.")
		
