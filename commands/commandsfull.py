from static import config,sendtext

def commandsfull(message, sender):
    	sendtext(sender, config['DEFAULT']['ai_name'] + ": This is a long one:"
        """
To play a song: <Keyword><Source> <Song Title> by <Artist>
Ex: BDeezer Call Me A Spaceman by Hardwell
Note: Spotify and Deezer are the only Sources currently.
Note: You do not have to include Artist but the more accurate you are the better the program will respond.
        """
