from static import config,sendtext

def commands(message, sender):
    	sendtext(sender, config['DEFAULT']['ai_name'] + ": Please visit http://tinyurl.com/MusicSharecommand \n" + "or \n" + "text back" + "\"BCommandsFull\"" + "for the complete command list texted to you."  )
