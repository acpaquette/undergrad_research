#!/usr/bin/env python
import sys
import os
import re
import tweepy
import csv
import configparser
import argparse
import datetime

class CustomStreamListener(tweepy.StreamListener):

    def __init__(self, output_file, time):
        super().__init__()
        self.default_output = os.path.split(os.path.splitext(output_file)[0])[-1]
        self.base_path = os.path.split(output_file)[0]
        self.output_file = self.update_output_file(self.default_output, self.base_path)
        self.start_time = time

    def on_status(self, status):
        full_text = ''
        full_name = ''
        coordinates = ''
        bounding_box = []
        quoted_status_id = 0
        retweeted_status = []
        hashtags = []
        urls = []
        user_mentions = []
        media = []

        if 'extended_tweet' in status._json.keys():
            full_text = status._json['extended_tweet']['full_text']
        elif 'retweeted_status' in status._json.keys():
            if 'extended_tweet' in status._json['retweeted_status'].keys():
                full_text = status._json['retweeted_status']['extended_tweet']['full_text']
        else:
            full_text = status.text

        if 'coordinates' in status._json.keys() and status._json['coordinates'] != None:
            coordinates = status._json['coordinates']['coordinates']

        if 'place' in status._json.keys() and status._json['place'] != None:
            full_name = status._json['place']['full_name']

        if 'place' in status._json.keys() and status._json['place'] != None:
            bounding_box = status._json['place']['bounding_box']['coordinates']

        if 'quoted_status_id' in status._json.keys() and status._json['quoted_status_id'] != None:
            quoted_status_id = status.quoted_status_id

        # Retweeted_Status is all information on retweeted tweet. Results in Big OUTPUTFILE.
        if 'retweeted_status' in status._json.keys() and status._json['retweeted_status'] != None:
            retweeted_status = status.retweeted_status.id

        if 'entities' in status._json.keys() and status._json['entities']['hashtags'] != None:
            hashtags = [i['text'] for i in status._json['entities']['hashtags']]

        if 'entities' in status._json.keys() and status._json['entities']['urls'] != None:
            urls = status._json['entities']['urls']

        if 'entities' in status._json.keys() and status._json['entities']['user_mentions'] != None:
            user_mentions = status._json['entities']['user_mentions']

        if 'entities' in status._json.keys() and status._json['entities'] != None:
            if 'media' in status._json['entities'].keys():
                media = status._json['entities']['media']

        # Clean the response text
        full_text = " ".join(full_text.split())
        full_text = re.sub(r'[\'\"]', '', full_text)
        full_text = full_text.encode('utf-8')
        # Writes to csv
        with open(self.output_file, 'a', encoding="utf8") as f:
            writer = csv.writer(f)
            writer.writerow([status.id, status.created_at, full_text, \
                             status.in_reply_to_user_id, status.user.id, \
                             status.user.name, status.user.screen_name, \
                             coordinates, full_name, bounding_box, \
                             quoted_status_id, retweeted_status, hashtags, urls, \
                             user_mentions, media, status.lang])


        # if check_time returns false, start a new collection file for the stream
        if check_time(self.start_time, datetime.datetime.now()) != True:
            self.start_time = datetime.datetime.now()
            self.output_file = self.update_output_file(self.default_output, self.base_path)

        return True

    @staticmethod
    def update_output_file(output_file, base_path):
        date = datetime.datetime.now()
        output_file = '{}/{}_{}'.format(base_path, date.strftime('%Y_%m_%d_%H'), output_file + '.csv')
        print("Generating output:", output_file)

        # Creation of output csv file
        with open(output_file, 'w', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['TweetID', 'Timestamp', 'Full_Text', 'In_Reply_To_User_ID', 'User_ID', 'User_Name', 'User_Screen_Name', 'Coordinates', 'Place', 'Bounding_Box', 'Quoted_Status_ID', 'Retweeted_Status', 'Hashtags', 'URLs', 'User_Mentions', 'Media', 'Language'])

        return output_file

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

    try:
        usernames = config['usernames']['usernames'].split(',')
    except:
        usernames = []

    return consumer_key, consumer_secret, access_key, access_secret, output_file, keywords, usernames

def generate_twitter_stream(config_file, start_time):
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
    consumer_key, consumer_secret, access_key, access_secret,\
    output_file, keywords, usernames = parse_config(config_file)

    #use variables to access twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)

    user_ids = [str(api.get_user(username).id) for username in usernames]

    # Define streamingAPI
    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(output_file, start_time))
    return streaming_api, keywords, user_ids

def start_stream(config_file, start_time):
    '''
    Starts a stream from a config file

    Parameters
    ----------
    config_file : str
                  Path to a config file
    '''
    streaming_api, keywords , user_ids= generate_twitter_stream(config_file, start_time)

    try:
        result = streaming_api.filter(track = keywords, follow = user_ids)
    except Exception as e:
        print("Stream Failed due to", e)

def check_time(start_time, tweet_time):
    # gets time of tweet when collected
    # gets master time from tweepyTimer
    # compares master time against tweet time to see if time
    # has past, change minute to hour, for hourly checks
    if start_time.hour == tweet_time.hour:
        return True

    print(start_time.hour, tweet_time.hour)
    return False

def main():
    start_time = datetime.datetime.now()

    #consumer key, consumer secret, access key, access secret.
    args  = parse_args()
    start_stream(args.config_file, start_time)

if __name__ == "__main__":
    main()
