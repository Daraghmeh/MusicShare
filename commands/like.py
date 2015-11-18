import traceback
from static import config, hottrack, sendtext, savesongs
import hashlib
import speakermanager
import party

curhash = ""
phones = []


def like(message, sender):
    try:
        song = speakermanager.getTrackInfo()
        hash = hashlib.md5((song[0] + song[2]).encode("UTF-8")).hexdigest()
        global curhash
        if curhash != hash:
            curhash = hash
            phones.clear()
        if sender not in phones:
            phones.append(sender)
            if hash not in hottrack:
                hottrack[hash] = [song[0], song[2], 0]
            hottrack[hash][2] += 1
            sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "You liked " + song[0] + " by " + song[1] + " song!")
            savesongs()
            if hottrack[hash][2] > party.getNumPlayers() / 2:
                speakermanager.playSong((speakermanager.curSource, song[0], song[2]))
        else:
            sendtext(sender,
                     config['DEFAULT']['ai_name'] + ": " + "You already liked " + song[0] + " by " + song[1] + " song!")
    except:
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "No song is playing :(")
        traceback.print_exc()
