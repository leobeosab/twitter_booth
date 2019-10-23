import twitter
import os

CONSUMER_KEY=os.environ['TAPI_CONSUMER_KEY']
CONSUMER_SECRET=os.environ['TAPI_CONSUMER_SECRET']
ACCESS_TOKEN_KEY=os.environ['TAPI_ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET=os.environ['TAPI_ACCESS_TOKEN_SECRET']

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

while True:
    print(api.GetMentions())
