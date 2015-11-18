from static import adminnumber,config,sendtext
import speakermanager
import party

adminmode = config['DEFAULT']['admin_mode'] == "true"

def skip(message, sender):
    try:
        if adminmode and sender == adminnumber:
            if party.getQueueSize() > 0:
                song = speakermanager.getTrackInfo()
                speakermanager.skip()
                sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "You sent a skip command for " + song[0] + " by " + song[2] + ".")
            else:
                sendtext(sender, config['DEFAULT']['ai_name']  + ": " + "No song to skip :(")
    except:
        sendtext(sender, config['DEFAULT']['ai_name']  + ": " +  "No song to skip :(")
