import sys
import tweepy
import csv

#consumer key, consumer secret, access key, access secret.
consumer_key=""
consumer_secret=""
access_key=""
access_secret=""

#use variables to access twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # Don't have to print to terminal, but nice
        print (status.author.screen_name, status.created_at, status.text.encode('utf-8'))
        # Writes to csv
        with open('OutputStreaming.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([status.author.screen_name, status.created_at, status.text.encode('utf-8')])

    # If error, keep streaming
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True

    # If timeout, keep streaming
    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True

# Creation of output csv file
with open('OutputStreaming.csv', 'w', encoding="utf8") as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'Date', 'Text'])

# Define streamingAPI
streamingAPI = tweepy.streaming.Stream(auth, CustomStreamListener())
# Call streamingAPI, which is stuck in while loop, not sure how to end w/o ctrl+c
streamingAPI.filter(track=['trump'])
