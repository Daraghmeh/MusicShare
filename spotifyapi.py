import json
from urllib.request import urlopen
import urllib.parse
from static import selectApi
import speakermanager


def search(searchTerm, artistName=None):
    """
    ~ Searches for the given search term using the spotify API ~
    :param searchTerm: the term to be searched. Ex: Beat it
    :param artistName: if given, the artist name to make the search more accurate. Ex: Michael Jackson
    :return: A dictionary containing the information and spotify link of the song (if it is found)

    Using the Spotify API, the song is acquired by receiving a JSON file and parsing
    through that to get the searchURI link, as well as a link to the song on spotify.
    """
    searchTerm = urllib.parse.quote(searchTerm)
    searchTag = "q=track:" + searchTerm
    if artistName is not None:
        if "feat." in artistName:
            artistName = artistName[:artistName.find('feat.')]
        elif "ft." in artistName:
            artistName = artistName[:artistName.find('ft.')]
        searchTag = searchTag + "%20artist:" + urllib.parse.quote(artistName)
    searchuri = "https://api.spotify.com/v1/search?" + searchTag + "&type=track"
    js = json.loads(urlopen(searchuri).read().decode('utf-8'))
    songs = js['tracks']['items']
    song = songs[0]
    artistNames = []
    for artist in song['artists']:
        artistNames.append(artist['name'].lower())
    if song['name'].lower() != searchTerm and artistName not in artistNames:
        for track in songs:
            artistNames = []
            for artist in song['artists']:
                artistNames.append(artist['name'].lower())
            if artist in artistNames:
                song = track
                break
    songName = song['name']
    trackUri = song['uri']
    artistUri = []
    for artist in song['artists']:
        artistUri.append(artist['id'])
    albumUri = song['album']['uri']
    postArg = {
        "source": "SPOTIFY",
        "type": "uri",
        "id": trackUri,
        "account": "theacex",
        "name": songName,
        "artistId": artistUri[0]
    }
    return postArg

def genreSearch2(artistName):
    """
    ~ Searches for the genre of the artist currently playing ~
    :param artistName: The artist to be searched
    :return: The genre of the artist
    Finds the artist using the Spotify API and parses
    the JSON files to find the genre value
    """
    artistName = urllib.parse.quote(artistName)
    type = "&type=artist,track"
    searchuri = "https://api.spotify.com/v1/search?q=" + artistName + type + "&market=US"
    js = json.loads(urlopen(searchuri).read().decode('utf-8'))
    genre = js['artists']['items']
    return genre

def genreSearch(artistName, playlistSize):
    """
    ~ Searches the genre of the current song playing and creates a playlist where the length
    is based on how many songs the user wants ~
    :param artistName: the given Artist. Ex: Drake
    :param playlistSize: The length of the playlist that is returned
    :return: An array containing the songs made by artists of the same/similar genre

    Acquires JSON files of the artist's similar artists and then searches
    for the top songs of those artists from the Spotify API
    """
    artistName = urllib.parse.quote(artistName)
    type = "&type=artist,track"
    searchuri = "https://api.spotify.com/v1/search?q=" + artistName + type + "&market=US"
    js = json.loads(urlopen(searchuri).read().decode('utf-8'))
    genre = js['artists']['items'][0]['genres']

    if len(genre) != 0:
        genre = "Not available"
        return genre
    searchTrack = speakermanager.getTrackInfo()
    ArtistID = search(searchTrack[0], artistName)
    relatedURI = "https://api.spotify.com/v1/artists/" + ArtistID['artistId'] + "/related-artists" # Drake ID
    jsRelatedArtists = json.loads(urlopen(relatedURI).read().decode('utf-8'))
    artistArray = []
    songArray = []
    artistIDArray = []
    arr = []
    while len(artistArray) <= playlistSize:
        for iter in jsRelatedArtists['artists']:
            artistArray.append(iter['id'])

    for artists in artistArray:
        relatedURI = "https://api.spotify.com/v1/artists/" + artists + "/related-artists"
        jsRelatedArtists = json.loads(urlopen(relatedURI).read().decode('utf-8'))
        artistIDArray.append(jsRelatedArtists['artists'][0]['id'])

    for iter in artistIDArray:
        topTracksURI = "https://api.spotify.com/v1/artists/" + iter +"/top-tracks?country=US"
        jsTopTracks = json.loads(urlopen(topTracksURI).read().decode('utf-8'))
        songArray.append(jsTopTracks['tracks'][0]['name'])
        arr.append([jsTopTracks['tracks'][0]['name'], jsTopTracks['tracks'][0]['artists'][0]['name']])
        if len(arr) >= playlistSize:
            break
    return arr

def validate(searchTerm, artistName=None):
    """
    ~ Validates that the song that is being searched exists ~

    :param searchTerm: term to be searched
    :param artistName: artist name if given
    :return: True or false, depending on if the search term is found

    Checks to see if a searchURI contains the song. IF the JSON
    file does not contain total tracks geater than zero, then
    false is returned.
    """
    searchTerm = urllib.parse.quote(searchTerm)
    searchTag = "q=track:" + searchTerm
    if artistName is not None:
        searchTag = searchTag + "%20artist:" + urllib.parse.quote(artistName)
    searchuri = "https://api.spotify.com/v1/search?" + searchTag + "&type=track"
    results = json.loads(urlopen(searchuri).read().decode('utf-8'))
    return results["tracks"]["total"] > 0
