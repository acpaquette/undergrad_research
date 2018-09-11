#!/usr/bin/env python
import sys
import tweepy
import csv
import configparser
import argparse
import datetime

class CustomStreamListener(tweepy.StreamListener):

    def __init__(self, output_file):
        super().__init__()
        self.output_file = output_file

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

#if __name__ == "__main__":
def __init__(time):

    global master_time
    master_time = time

    #consumer key, consumer secret, access key, access secret.
    args  = parse_args()

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
    with open(get_filename(), 'w', encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(['TweetID', 'Timestamp', 'Tweet_Text_Content', 'UserID', 'User_Name', 'Country State City', 'Likes'])

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
    try:
        result = streaming_api.filter(track=keywords)
    except Exception as e:
        print("Stream Failed due to", e)

if __name__ == "__main__":
    args = parse_args()
    print("Started", args.config_file)

    start_stream(args.config_file)
    # Call streamingAPI, which is stuck in while loop, not sure how to end w/o ctrl+c
    streaming_api.filter(track=['car'])

def check_time(tweet_time):
    #print(tweet_time.minute)
    #print(master_time.minute)
    #gets time of tweet when collected
    #gets master time from tweepyTimer
    #compares master time against tweet time to see if time has past, change minute to hour, for hourly checks
    if(master_time.minute == tweet_time.minute):
        return True
    return False

def get_filename():
    #concatenates file name together for dynamic naming based on master time
    name = 'output_machine1_time'
    ext = '.csv'
    return name + str(master_time.minute) + ext
