from static import config,sendtext
import speakermanager

def system(message, sender):
    info = speakermanager.getSystemSettings()
    message = """
Name: %(name)s
Type: %(type)s
Software Version: %(softwareVersion)s
Serial Number: %(serialNumber)s
Mac Address: %(macAddress)s
IP Address: %(ipAddress)s
        """
    sendtext(sender, config['DEFAULT']['ai_name'] + ": System Info" + message%info)
    