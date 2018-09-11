#!/usr/bin/env python
import sys
import tweepy
import csv
import configparser
import argparse

class CustomStreamListener(tweepy.StreamListener):

    def __init__(self, output_file):
        super().__init__()
        self.output_file = output_file

    def on_status(self, status):
        # Don't have to print to terminal, but nice
        # print(status.author.screen_name, status.created_at, status.text.encode('utf-8'))
        # Writes to csv
        with open(self.output_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([status.author.screen_name, status.created_at, status.text.encode('utf-8')])

    # If error, keep streaming
    def on_error(self, status_code):
        # TODO: Add write to some error file
        print(self.output_file)
        print('Encountered error with status code:', status_code, file = sys.stderr)
        return True

    # If timeout, keep streaming
    def on_timeout(self):
        print('Timeout...', file = sys.stderr)
        return True

def parse_args():
    '''
    Parses the command line arguments for the script

    Returns
    -------

    args : object
           Python arg parser object
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('config_file', type=str, help='Ini config file to setup the twitter stream.')
    args = parser.parse_args()
    return args

def parse_config(config_file):
    '''
    Parses a twitter streaming config file

    Parameters
    ----------
    config_file : str
                  Path to a config file

    Returns
    -------
    consumer_key : str
                   Consumer key from the config file

    consumer_secret : str
                      Consumer secret from the config file

    access_key : str
                 Access key from the config file

    access_secret : str
                    Access secret from the config file

    keywords : list
               List of keywords gathered from a string in config_file
    '''
    config = configparser.ConfigParser()
    config.read(config_file)

    consumer_key = config['keys']['consumer_key']
    access_key = config['keys']['access_key']

    consumer_secret = config['secrets']['consumer_secret']
    access_secret = config['secrets']['access_secret']

    output_file = config['output']['output_file']

    keywords = config['keywords']['keywords'].split(',')

    return consumer_key, consumer_secret, access_key, access_secret, output_file, keywords

def generate_twitter_stream(config_file):
    '''
    Generates a twitter stream from a config file

    Parameters
    ----------
    config_file : str
                  Path to a config file

    Returns
    -------
    streaming_api : object
                    Twitter streaming api object
    '''
    consumer_key, consumer_secret, access_key, access_secret, output_file, keywords = parse_config(config_file)

    #use variables to access twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # Creation of output csv file
    with open(output_file, 'w', encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(['Author', 'Date', 'Text'])

    # Define streamingAPI
    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(output_file))
    return streaming_api, keywords

def start_stream(config_file):
    '''
    Starts a stream from a config file

    Parameters
    ----------
    config_file : str
                  Path to a config file
    '''
    streaming_api, keywords = generate_twitter_stream(config_file)
    # Call streamingAPI, which is stuck in while loop, not sure how to end w/o ctrl+c
    try:
        result = streaming_api.filter(track=keywords)
    except Exception as e:
        print("Stream Failed due to", e)

if __name__ == "__main__":
    args = parse_args()
    print("Started", args.config_file)

    start_stream(args.config_file)
