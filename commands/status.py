import speakermanager
from static import config,sendtext

def status(message, sender):
    volume = speakermanager.getVolume()
    bass = speakermanager.getBass()
    try:
        songName = speakermanager.getTrackInfo()
    except:
        songName = False
    message = """
Volume: %(volume)d
Bass: %(bass)s
Song: %(song)s
"""
    bassCap = speakermanager.getBassCapabilities()
    if not songName:
        song = "None"
    else:
        song = songName[0] + " by " + songName[2]
        data = {"volume": volume, "bass": str(bass) + " out of " + bassCap[1], "song": song}
        sendtext(sender, config['DEFAULT']['ai_name'] + ": Basis Status" + message%data)
