from static import sendtext
import speakermanager

def activate(message, sender):
    speakermanager.simulateKeyPress(message.upper())
    sendtext(sender, message.upper())
