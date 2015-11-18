from urllib import request
import xml.etree.ElementTree
import json

import deezerapi
import spotifyapi
from static import selectApi
from static import config
from static import speakerOn
import party

speakerAddress = config['speaker']['speakerAddress']
webViewAddress = config['speaker']['webViewAddress']

skipping = False
forceSkip = False


curSource = "deezer"


def isPlaying():
    """
    ~ Checks to see if the speaker is playing a song ~
    :return: the status of the speaker which is playing and not skipping
    """
    if forceSkip:
        return False
    response = str(sendGet(speakerAddress + "now_playing"))
    playing = (response.find("INVALID_SOURCE") == -1)
    if playing:
        playing = (response.find("AUX") == -1)
    return playing and not skipping

def setVolume(volume):
    """
    ~ sets the Volume of the speaker
    :param volume: An integer to be set for the vulume

    Takes the volume and sends it to the speaker using
    the sendPost() method
    """
    volume = int(volume)
    vol_max = int(config['volume']['volume_max'])
    vol_min = int(config['volume']['volume_min'])
    volume = min(vol_max, max(vol_min, volume))
    sendPost(speakerAddress + "volume", "<volume>" + str(volume) + "</volume>")

def playSong(songItem):
    """
    ~ Plays the song that is in the queue
    :param songItem: The song that is going to be played
    Sends the queued song to the speaker to be played
    """
    songName = songItem[0]
    artistName = songItem[1]
    source = songItem[2]
    global curSource
    curSource = source
    if not artistName:
        artistName = None
    response = searchForSong(source, songName, artistName)
    sendSong(selectApi%response)

def skip():
    """
    ~Skips the current song playing
    Admin functionality only where the current
    song is skipped and moves onto the next song
    in the queue if one is present
    """
    #global skipping
    #skipping = True
    #party.playNextSong()
    global forceSkip
    forceSkip = True

def getVolume():
    """
    ~Gets the current volume of the speaker
    Uses sendGet() to receive information
    about the volume of the speaker and returns
    that from the Bose API
    """
    response = sendGet(speakerAddress + "volume").decode('utf-8')
    tree = xml.etree.ElementTree.fromstring(response)
    volume = tree.find('actualvolume').text
    return int(volume)

def getBass():
    """
    ~ Gets the current base of the speaker ~
    Similar to getVolume() the base is
    acquired from sendGet() to the speaker
    address and finding it through the Bose API
    """
    response = sendGet(speakerAddress + "bass").decode('utf-8')
    tree = xml.etree.ElementTree.fromstring(response)
    bass = tree.find('actualbass').text
    return int(bass)

def getBassCapabilities():
    """
    ~ Gets the range that the bass can link ~
    """
    response = sendGet(speakerAddress + "bassCapabilities").decode('utf-8')
    tree = xml.etree.ElementTree.fromstring(response)
    min = tree.find('bassMin').text
    max = tree.find('bassMax').text
    return [min,max]

def clear():
    """
    ~ Clears the speaker of songs and the queue of songs ~
    Simulates pressing the power key which clears the queue of songs
    and the number of players + boos in the system
    """
    simulateKeyPress("POWER")
    if speakerOn:
        simulateKeyPress("POWER")
    simulateKeyPress("AUX_INPUT")
    simulateKeyPress("AUX_INPUT")
    party.curPlayer = 0
    party.players = []
    party.queues = {}
    party.boos = {}

def getTrackInfo():
    """
    ~ Gets the information (song name, artist) of the current song playing ~
    :return: returns an array containing four items: the track, it's album, the artist, and album art
    From the speaker, we get information regarding the track, artist, album, and art and put that into
    an array
    """
    response = sendGet(speakerAddress + "now_playing").decode("UTF-8")

    tree = xml.etree.ElementTree.fromstring(response)
    track = tree.find('track').text
    artist = tree.find('artist').text
    album = tree.find('album').text
    art = tree.find('art').text

    info = [track, album, artist, art]
    return info


# web view


def sendToWebView(obj):
    sendPost(webViewAddress + "getPost.html", json.dumps(obj))


# http interaction functions

def sendSong(songStr):
    """
    ~Sends song to speaker

    Sends the song to the speaker address
    which will be put in the queue
    """
    sendPost(speakerAddress + "select", songStr)
    global forceSkip
    forceSkip = False

def searchForSong(source, songName, artistName = None):
    """
    ~ Searches for the song in Spotify or Deezer
    :param source: The music platform to be searched in.
    :param songName: The name of the song to be searched.
    :param artistName: The name of the artist to help clarify the search
    :return: The song if found

    Searches the song name in either Spotify or Deezer, based ont he source
    """
    if source.lower() == "deezer":
        return deezerapi.search(songName, artistName)
    elif source.lower() == "spotify":
        return spotifyapi.search(songName, artistName)

def simulateKeyPress(key):
    """
    ~ Simulates pressing whatever key is passed in Ex: Increase Volume Button
    :param key: The key that is being siulated by pressing

    """
    args = {'key_state':'press', 'key_value':key, 'sender': 'Gabbo'}
    post = """<key state="%(key_state)s" sender="%(sender)s">%(key_value)s</key>"""
    sendPost(speakerAddress + "key", post%args)
    args['key_state'] = 'release'
    sendPost(speakerAddress + "key", post%args)


# Low-level http request sender functions


def getSystemSettings():
    response = sendGet(speakerAddress + "info")
    tree = xml.etree.ElementTree.fromstring(response)
    name = tree.find('name').text
    type = tree.find('type').text
    softwareVersion = tree.find('components').find('component').find('softwareVersion').text
    serialNumber = tree.find('components').find('component').find('serialNumber').text
    macAddress = tree.find('networkInfo').find('macAddress').text
    ipAddress = tree.find('networkInfo').find('ipAddress').text
    return {
        'name': name,
        'type': type,
        'softwareVersion': softwareVersion,
        'serialNumber': serialNumber,
        'macAddress': macAddress,
        'ipAddress': ipAddress
    }

def sendPost(address, postStr):
    post = postStr.encode("UTF-8")
    return request.urlopen(address, post).read()

def sendGet(address):
    return request.urlopen(address).read()
