#!/usr/bin/env python
import sys
import tweepy
import csv
import configparser
import argparse
import datetime

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # Don't have to print to terminal, but nice
        print(status.id, status.created_at, status.text.encode('utf-8'), status.user.id, status.user.screen_name, status.user.location, status.user.favourites_count)
        # Writes to csv
        with open(get_filename(), 'a') as f:
            writer = csv.writer(f)
            writer.writerow([status.id, status.created_at, status.text.encode('utf-8'), status.user.id, status.user.screen_name, status.user.location, status.user.favourites_count])

        #if check_time returns false, exit tweet collection 'while' loop
        if(check_time(datetime.datetime.now()) != True):
            return False

    # If error, keep streaming
    def on_error(self, status_code):
        print('Encountered error with status code:', status_code, file = sys.stderr)
        # print >> sys.stderr, 'Encountered error with status code:', status_code
        return True

    # If timeout, keep streaming
    def on_timeout(self):
        print('Timeout...', file = sys.stderr)
        # print >> sys.stderr, 'Timeout...'
        return True


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('config_file', type=str, help='Ini config file to setup the twitter stream.')
    args = parser.parse_args()
    return args

def parse_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    consumer_key = config['keys']['consumer_key']
    access_key = config['keys']['access_key']

    consumer_secret = config['secrets']['consumer_secret']
    access_secret = config['secrets']['access_secret']

    return consumer_key, consumer_secret, access_key, access_secret

#if __name__ == "__main__":
def __init__(time):

    global master_time
    master_time = time

    #consumer key, consumer secret, access key, access secret.
    args  = parse_args()

    consumer_key, consumer_secret, access_key, access_secret = parse_config(args.config_file)

    #use variables to access twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # Creation of output csv file
    with open(get_filename(), 'w', encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(['TweetID', 'Timestamp', 'Tweet_Text_Content', 'UserID', 'User_Name', 'Country State City', 'Likes'])

    # Define streamingAPI
    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener())
    # Call streamingAPI, which is stuck in while loop, not sure how to end w/o ctrl+c
    streaming_api.filter(track=['car'])

def check_time(tweet_time):
    #gets time of tweet when collected
    ttime = tweet_time.minute
    #gets master time from tweepyTimer
    mtime = master_time.minute
    #print(ttime)
    #print(mtime)
    #compares master time against tweet time to see if time has past
    if(mtime == ttime):
        return True
    return False

def get_filename():
    #concatenates file name together for dynamic naming based on master time
    name = 'output'
    ext = '.csv'
    return name + str(master_time.minute) + ext
