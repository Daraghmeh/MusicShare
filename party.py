import collections, copy, time
from static import sendtext
from static import config
from static import hottrack
import speakermanager
import hotsongs
 
default_song_name = config['DEFAULT']['songname']
 
players = []
queues = {}
boos = {}
 
curPlayer = 0
songsplayed = dict()
 
 
def getNumPlayers():
    """
    ~ Getter method to get the number of players participating
    :return: The amount of players
    """
    return len(players)
 
def getQueueSize():
    """
    ~ Gets the size of the queue of songs
    :return: The size of the queue in integer form
    Iterates through the queue to get the length
    """
    length = 0
    for q in queues:
        length += len(q)
    return length
 
def queuesong(sender, source, songname, artistname=None):
    """
    ~ Queues the song to be in the in the queue ~
    :param sender: The speaker address
    :param source: The phone number that is requesting it
    :param songname: The name of the song to queue
    :param artistname: The artist of the song

    Queues the song which is sent from the players.
    If the sender is not in players, then they
    are placed in the player array. Will message
    the player back with the confirmation of it
    being queued.

    """
    if sender not in players:
        players.append(sender)
        queues[sender] = collections.deque()
        boos[sender] = False
    queues[sender].append((songname, artistname, source))
    message = "Song queued: " + songname
    if artistname is not None:
        message = message + " by " + artistname
    sendtext(sender, message)
 
def setBoo(phoneNum):
    """
    ~ Increments the boo counter ~
    :param phoneNum:
    :return:
    """
    booed = False
    if phoneNum in boos:
        booed = boos[phoneNum]
    boos[phoneNum] = True
    return not booed
 
def clearBoos():
    """
    ~ Clears the boo counter ~
    Removes boos from the boo array
    for every player
    """
    for p in players:
        boos[p] = False
 
def incrementPlayer():
    """
    ~ Increments the player count by
    adding another player ~
    """
    global curPlayer
    curPlayer = (curPlayer + 1) % len(players)
 
def playNextSong():
    """
    ~ Plays the next song ~
    Plays the next song queued
    and clears the boo array
    and alerts the player
    who queued the song that his/her
    song will be played next
    """
    speakermanager.playSong(getNextSong())
    clearBoos()
    time.sleep(5)
    ns = acquireNextSong()
    if ns:
        sendtext(ns[0], "Your song '" + ns[1][0] + "' will be playing next!")
    #updateWebView() # WEB VIEW
 
def acquireNextSong():
    """
    ~ Acquires the next song ~
    :return: A double array that consists of the phone number and the current place in the song
    Immediate song from the queue is retrieved to be the next song to play from the speakers
    """
    aCurPlayer = curPlayer
    for i in range(len(players)):
        phoneNum = players[aCurPlayer]
        aCurQueue = queues[phoneNum]
        if len(aCurQueue)>0:
            return (phoneNum, aCurQueue[0])
        aCurPlayer = (aCurPlayer + 1) % len(players)
    return None
 
def getNextSong():
    """
    ~ Gets the next song fot the queue ~
    Difference between this method and acquireNextSong() is that
    this method gets the song from the player
    """
    if len(players)<1:
        print("waiting for players...")
        while len(players)<1:
            time.sleep(1)
        print("player found!")
    while True:
        curQueue = queues[players[curPlayer]]
        if len(curQueue)>0:
            incrementPlayer()
            return curQueue.popleft()
        print("player '" + players[curPlayer] + "' has no songs queued, skipping...")
        if getQueueSize() == 0 and len(hottrack) > 0:
            addHotList()
            return
        elif getQueueSize() == 0 and len(hottrack) == 0:
            while getQueueSize() == 0:
                time.sleep(1)
        incrementPlayer()
        time.sleep(1)
 
def addHotList():
    """
    ~ Adds to permanent top ten playlist ~
    :return: Returns the length of the the hot track
    """
    if len(hottrack) > 0:
        tracks = hotsongs.build_playlist(hottrack)
        for track in tracks:
            queuesong(None, "Spotify", track[0], track[1])
    return len(hottrack)
 
# send updated state to web view
def updateWebView():
    """
    ~ Connection fpr dumping JSON for Django ~
    """
    deepQueues = copy.deepcopy(queues)
    deepCurPlayer = curPlayer
 
    webQueue = []
 
    noQueueRun = 0
    while noQueueRun<=len(players):
        p = players[deepCurPlayer]
        if len(deepQueues[p]) > 0:
            deepSong = deepQueues[p].popleft()
            webQueue.append((p, deepSong))
            noQueueRun = 0
        else:
            noQueueRun += 1
        deepCurPlayer = (deepCurPlayer + 1) % len(players)
 
    data = (webQueue, speakermanager.getTrackInfo()) # convert to JSON or XML, send to web view server
    speakermanager.sendToWebView(data)


