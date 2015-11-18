from static import config,sendtext
import party
 
def list(message, sender):
    if party.getQueueSize() > 0:
        for q in party.queues:
            msg =  config['DEFAULT']['ai_name'] + ": " + "Songs in queue:\n"
            for song in party.queues[q]:
                if song[1] is not None:
                    msg += song[0] + " by " + song[1] + "\n"
                else:
                    msg += song[0]
        sendtext(sender, msg)
    else:
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "No song in queue :(")


