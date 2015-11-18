from party import addHotList
from static import config,sendtext

def top(message, sender):
    len = addHotList()
    if len > 0:
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " "Queued songs from hot playlist!")
    else:
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " "No songs in hot playlist :(")
