from static import config,sendtext
import speakermanager

def input(message, sender):
    if message.strip().upper() == "AUX":
        speakermanager.simulateKeyPress("AUX_INPUT")
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "You sent an Input AUX command.")
    if message.index("preset") > -1:
        if not len(message) == 8:
            sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "Invalid Preset, acceptable range 1-6.")
        else:
            speakermanager.simulateKeyPress(message.replace(" ", "_").upper())
            sendtext(sender, message.replace(" ", "_").upper())
