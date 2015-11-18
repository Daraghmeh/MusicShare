import json
import urllib.parse
from urllib.request import urlopen
from static import config

apiKey = config['deezer']['apiKey']
sourceAccount = config['DEFAULT']['sourceAccount']


def search(searchterm, artist = None):
    """
    ~ Searches for the given search term using the Deezer API ~
    :param searchTerm: the term to be searched. Ex: Beat it
    :param artistName: if given, the artist name to make the search more accurate. Ex: Michael Jackson
    :return: A dictionary containing the information and Deezer link of the song (if it is found)

    Using the Deezer API, the song is acquired by receiving a file and parsing
    through that to get the searchURI link, as well as a link to the song on Deezer.
    """

    searchuri = "https://api.deezer.com/search?access_token=" + apiKey + "&q="
    query = "track:\"" + searchterm + "\""
    if artist is not None:
        query = query + "%20artist:\"" + artist + "\""
    query = urllib.parse.quote(query)
    response = urlopen(searchuri+query).read().decode('utf-8')
    results = json.loads(response)
    song = results['data'][0]
    if song['title'].lower() != searchterm and song['artist']['name'].lower() != artist:
        for track in results['data']:
            if track['artist']['name'].lower() == artist:
                song = track
                break
    songName = song['title']
    id = song['id']
    artistId = song['artist']['id']
    # source, type, id, account, name
    postArg = {
        "source": "DEEZER",
        "type": "track",
        "id": id,
        "account": sourceAccount,
        "name": songName
    }
    return postArg

def validate(searchterm, artist = None):
    """
    ~ Validates that the song that is being searched exists ~

    :param searchTerm: term to be searched
    :param artistName: artist name if given
    :return: True or false, depending on if the search term is found

    Checks to see if a searchURI contains the song. IF the
    file does not contain total tracks geater than zero, then
    false is returned.
    """
    searchuri = "https://api.deezer.com/search?access_token=" + apiKey + "&q="
    query = "track:\"" + searchterm + "\""
    if artist is not None:
        query = query + "%20artist:\"" + artist + "\""
    query = urllib.parse.quote(query)
    response = urlopen(searchuri+query).read().decode('utf-8')
    results = json.loads(response)
    return results["total"] > 0

