import importlib
import os
import sys
import traceback

from static import config
from static import sendtext
import static
import server
# import command folder
sys.path.append(os.path.join(os.path.dirname(__file__), "commands"))


def handle(command, message, sender):
    """
    ~ Handles the commands to the speaker ~
    :param command: The command to be sent. The first word of the message  Ex: BoseVolume 20
    :param message: The content AFTER the commmand. Ex: Bdeezer Sandstorm is just Sanstorm for the message
    :param sender: The phone number it is being sent from

    Checks to see if command + "py" exists. Then it imports that file and invokes the method
    inside that file. Otherwise it sends the player a message saying the command doesn't exist.
    """

    if static.adminnumber is None:
        static.adminnumber = sender
    # the command is handled by a file and function named after itself
    # BREAKS IF COMMAND IS FIRST WORD OF A POSIBLE SONG NAME
    keyword = config['DEFAULT']['keyword']
    command = command[len(keyword):]
    try:
        target_file = os.path.join(os.path.dirname(__file__), "commands/" + command + '.py')
        if os.path.isfile(target_file):
            server.validatestatus()
            module = importlib.import_module(command + '')
            getattr(module, command)(message, sender)
        else:  # if file doesn't exist, assume queue of song
            # fabricate original message
            #message = command + " " + message
            #module = importlib.import_module('song')
            #getattr(module, 'song')(message, sender)
            sendtext(sender, config['DEFAULT']['ai_name'] + ": " +  "Sorry, no such command.  Please text" + "\"BHelp\"" + "for command list.")
    except Exception as e:
        print('Error handling command')
        print('error:')
        traceback.print_exc()
