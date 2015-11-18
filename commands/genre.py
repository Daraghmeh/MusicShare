__author__ = 'sadaf345'
import spotifyapi
import re
import speakermanager
from static import config,sendtext
import party


def genre(message, sender):
    playlistSize = int(message)
    try:
        info = speakermanager.getTrackInfo()
        genre = spotifyapi.genreSearch(info[2], playlistSize)
        songOnly = []
        for iter in genre:
            party.queuesong(sender, "spotify", iter[0], iter[1])
            songOnly.append(iter[0])

        #sendtext(sender, "Playlist that matches your song: " + ','.join(songOnly))
    except:
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "Cannot generate playlist, is a song playing?")
