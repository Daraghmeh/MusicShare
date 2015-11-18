import os
import configparser
from twilio.rest import TwilioRestClient

# config
config = configparser.ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), 'CONFIG.ini')
config.read(config_file)
sid = config['twilio']['sid']
token = config['twilio']['token']
from_ = config['twilio']['number']

songconfig = configparser.ConfigParser()
songconfig.read(os.path.join(os.path.dirname(__file__), 'topsongs.ini'))
if not songconfig.has_section("DEFAULT"):
    songconfig["DEFAULT"] = {}
    songconfig.write(open("topsongs.ini", "w"))
else:
    if len(songconfig["DEFAULT"]) > 0:
        global hottrack
        for key,value in songconfig["DEFAULT"]:
            hottrack[key] = value

# twilio
twilio = TwilioRestClient(sid, token)

# command required variables
booCount = 0

# bose format
# format with dictionary of:
# source, type, id, account, name
selectApi = """
<ContentItem source="%(source)s" type="%(type)s" location="%(id)s"
    sourceAccount="%(account)s" isPresetable="true">
    <itemName>%(name)s</itemName>
</ContentItem>"""

# speaker state
speakerOn = True

# data
hottrack = dict()
adminnumber = None


def sendtext(to, message):
    """
    ~ Sends message to the speaker address ~
    :param to: The address to send the content to
    :param message: The content of the message
    :return: N/A
    Uses Twilio API to structure messages with a to, from, and a
    body which contains the message
    """
    if to is not None:
        twilio.messages.create(
            to=to,
            from_=from_,
            body=message
        )
    print(message)


def savesongs():
    """
    ~ Save songs for the top ten playlist ~
    """
    for song in hottrack:
        songconfig['DEFAULT'][song[0]] = song[1]
    songconfig.write(open("topsongs.ini", "w"))

