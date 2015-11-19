from static import config,sendtext
import speakermanager
import static
 
def power(message, sender):
    if static.speakerOn:
        speakermanager.simulateKeyPress("POWER")
    sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "Power")
    static.speakerOn = not static.speakerOn
