from escpos.printer import Usb, Dummy
from escpos.image import EscposImage

import subprocess
import twitter
import os, time

CONSUMER_KEY=os.environ['TAPI_CONSUMER_KEY']
CONSUMER_SECRET=os.environ['TAPI_CONSUMER_SECRET']
ACCESS_TOKEN_KEY=os.environ['TAPI_ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET=os.environ['TAPI_ACCESS_TOKEN_SECRET']

PIC_COMMAND="/usr/bin/fswebcam tmp.jpg --scale 640x480 --rotate 90 --save out.jpg"

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

# Note this is all really hacky

class Photobooth:
    api = None
    printer = None
    lastMention = None

    def __init__(self, api):
        self.api = api
        self.printer = Usb(0x0416, 0x5011, 0, 0x81, 0x01)
        self.lastMention = self.api.GetMentions()[0].AsDict()

    def StartBooth(self):
        while True:
            if self.CheckForNewMention():
                print("New mention! by " + self.lastMention['user']['screen_name'])
                self.SnapAndPrint()
            time.sleep(5)

    def CheckForNewMention(self):
        recentMention = api.GetMentions()[0].AsDict()
        if self.lastMention['id'] != recentMention['id']:
            self.lastMention = recentMention
            return True
        return False

    def SnapAndPrint(self):
        subprocess.run(PIC_COMMAND.split(" ")) 
        dummy = Dummy()
        
        dummy.text("\n\n\nBravoLT - GRPS - 2019\n\n\n")
        dummy.image("out.jpg")
        dummy.text("\n\n\nBravoLT - GRPS - 2019")

        self.printer._raw(dummy.output)

booth = Photobooth(api)
booth.StartBooth()
