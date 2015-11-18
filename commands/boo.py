from static import config,sendtext
import static
import party
import speakermanager
 
def boo(message, sender):
    try:
        if party.setBoo(sender):
            static.booCount += 1
            song = speakermanager.getTrackInfo()
            if static.booCount > party.getNumPlayers() / 2:
                sendtext(sender, config['DEFAULT']['ai_name'] + ": " + song[0] + " by " + song[1] + " has been booed")
                static.booCount = 0
                speakermanager.skip()
            else:
                sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "You already booed " + song[0] + " by " + song[1] + "." " BE NICE.")
     
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "You sent a boo command for " + song[0] + " by " + song[1] + ".")
    except:
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "There's no song to boo!")

