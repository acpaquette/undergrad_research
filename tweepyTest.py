#!/usr/bin/env python
import sys
import tweepy
import csv
import configparser
import argparse

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # Don't have to print to terminal, but nice
        print(status.author.screen_name, status.created_at, status.text.encode('utf-8'))
        # Writes to csv
        with open('OutputStreaming.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([status.author.screen_name, status.created_at, status.text.encode('utf-8')])

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

if __name__ == "__main__":
    #consumer key, consumer secret, access key, access secret.
    args  = parse_args()

    consumer_key, consumer_secret, access_key, access_secret = parse_config(args.config_file)

    #use variables to access twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # Creation of output csv file
    with open('OutputStreaming.csv', 'w', encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(['Author', 'Date', 'Text'])

    # Define streamingAPI
    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener())
    # Call streamingAPI, which is stuck in while loop, not sure how to end w/o ctrl+c
    streaming_api.filter(track=['trump'])
