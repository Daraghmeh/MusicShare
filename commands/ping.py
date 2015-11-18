from static import adminnumber,config,sendtext

adminmode = config['DEFAULT']['admin_mode'] == "true"

def ping(message, sender):
    if adminmode and sender == adminnumber:
    	sendtext(sender, config['DEFAULT']['ai_name'] + ": " +  config['DEFAULT']['master_name'][-4:] + " , I received your message: " + message)
	else:
    	sendtext(sender, config['DEFAULT']['ai_name'] + ": " + "I received your message: " + message)
