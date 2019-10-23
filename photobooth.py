from ecapture import ecapture as ec
from escpos.printer import Usb

import twitter
import os, time

CONSUMER_KEY=os.environ['TAPI_CONSUMER_KEY']
CONSUMER_SECRET=os.environ['TAPI_CONSUMER_SECRET']
ACCESS_TOKEN_KEY=os.environ['TAPI_ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET=os.environ['TAPI_ACCESS_TOKEN_SECRET']

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

# Note this is all really hacky

class Photobooth:
    api = None
    lastMention = None

    def __init__(self, api):
        self.api = api
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
        ec.capture(0, False, "tmp.jpg")

booth = Photobooth(api)
booth.SnapAndPrint()
#booth.StartBooth()
