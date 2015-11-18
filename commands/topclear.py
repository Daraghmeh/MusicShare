from party import addHotList
from static import config,sendtext
import party

def topclear(message, sender):
    party.curPlayer = 0
    party.players = []
    party.queues = {}
    party.boos = {}
    len = addHotList()
    if len > 0:
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " "Cleared songs from hot playlist!")
    else:
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " "No songs in hot playlist :(")
