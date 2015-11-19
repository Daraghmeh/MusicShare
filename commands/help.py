from static import config,sendtext

def help(message, sender):
    	sendtext(sender, config['DEFAULT']['ai_name'] + ": Please visit http://tinyurl.com/MusicSharecommand \n" + "or text back " + "\"BHelpList\"" + "for the complete command list texted to you."  )
