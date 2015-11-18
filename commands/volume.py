from static import config,sendtext
import speakermanager

def volume(message, number):
    curVol = speakermanager.getVolume()
    if message.isdigit():
        speakermanager.setVolume(message)
        sendtext(number, config['DEFAULT']['ai_name'] + ": " + "Result volume: " + str(message))
    elif message == "up":
        speakermanager.setVolume(curVol + 5)
        sendtext(number, config['DEFAULT']['ai_name'] + ": " + "You sent a volume up command")
    elif message == "down":
        speakermanager.setVolume(curVol - 5)
        sendtext(number, config['DEFAULT']['ai_name'] + ": " + "You sent a volume down command")
