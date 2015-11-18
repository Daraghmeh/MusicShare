import deezerapi
import json
from urllib.request import urlopen
import urllib.parse
from static import sendtext
from static import config
import party


def deezer(message, sender):
    msgfrag = message.split(' ', 1)
    command = msgfrag[0]
    message = ""
    if len(msgfrag) == 2:
        message = msgfrag[1].strip() or ""

    if command == "lyric":
        handleLyricSearch(message, sender)
    else:
        handleSongSearch(command + " " + message, sender)



def handleSongSearch(message, sender):
    songname = message
    artistname = None
    splitter = "by"
    if message.find(splitter) > -1:
        songname = message[:message.find(splitter)].strip()
        artistname = message[message.find(splitter)+len(splitter):].strip()
    if deezerapi.validate(songname, artistname):
        party.queuesong(sender, "deezer", songname, artistname)
    else:
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "Unable to find song: " + songname + "on Deezer.")
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "To send a song follow this format <Keyword><Source> <Song Title> by <Artist>" + "\n" + "For more commands please text" + "\"BCommands\"")



def handleLyricSearch(message, sender):
    apiKey = config['musixmatch']['apikey']  # 2000 hits per day
    searchTerm = urllib.parse.quote(message)
    url = "http://api.musixmatch.com/ws/1.1/track.search?q_lyrics=" + searchTerm + "&apikey=" + apiKey
    response = urlopen(url)
    tracks = json.loads(response.read().decode('utf-8'))['message']['body']['track_list']
    tracksFound = len(tracks)
    if tracksFound > 0:
        firstSong = tracks[0]['track']
        trackName = firstSong['track_name']
        artistName = firstSong['artist_name']
        party.queuesong(sender, "deezer", trackName, artistName)
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "Found " + trackName + " by " + trackName + " ." )
    else:
        sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "Your song" + message + "was not found!")
