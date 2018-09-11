#!/usr/bin/env python
import sys
import os
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
        # Don't have to print to terminal, but nice
        # print(status.id, status.created_at, status.text.encode('utf-8'), status.user.id, status.user.screen_name, status.user.location, status.user.favourites_count)
        # Writes to csv
        with open(self.output_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([status.id, status.created_at, status.text.encode('utf-8'), status.user.id, status.user.screen_name, status.user.location, status.user.favourites_count])

        # if check_time returns false, start a new collection file for the stream
        if check_time(self.start_time, datetime.datetime.now()) != True:
            CustomStreamListener.combine_time_files(self.output_file, self.base_path)
            self.start_time = datetime.datetime.now()
            self.output_file = self.update_output_file(self.default_output, self.base_path)

        return True

    @staticmethod
    def update_output_file(output_file, base_path):
        date = datetime.datetime.now()
        output_file = '{}/{}_{}_{}_{}_{}_{}'.format(base_path, str(date.year), \
                                                 str(date.month), str(date.day), \
                                                 str(date.hour), str(date.minute), output_file + '.csv')
        print("Generating output:", output_file)

        # Creation of output csv file
        with open(output_file, 'w', encoding="utf8") as f:
            writer = csv.writer(f)
            writer.writerow(['TweetID', 'Timestamp', 'Tweet_Text_Content', 'UserID', 'User_Name', 'Country State City', 'Likes'])

        return output_file

    @staticmethod
    def combine_time_files(file, base_path):
        file_split = file.split('_')
        composite_file = '{}_{}_{}_{}_composite.csv'.format(*file_split[0:4])
        os.system('cat ' + file + ' >> ' + composite_file)
        os.system('rm ' + file)

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
    consumer_key, consumer_secret, access_key, access_secret, output_file, keywords = parse_config(config_file)

    #use variables to access twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # Define streamingAPI
    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(output_file, start_time))
    return streaming_api, keywords

def start_stream(config_file, start_time):
    '''
    Starts a stream from a config file

    Parameters
    ----------
    config_file : str
                  Path to a config file
    '''
    streaming_api, keywords = generate_twitter_stream(config_file, start_time)
    try:
        result = streaming_api.filter(track=keywords)
    except Exception as e:
        print("Stream Failed due to", e)

def check_time(start_time, tweet_time):
    # gets time of tweet when collected
    # gets master time from tweepyTimer
    # compares master time against tweet time to see if time
    # has past, change minute to hour, for hourly checks
    if start_time.minute == tweet_time.minute:
        return True

    print(start_time.minute, tweet_time.minute)
    return False

def main():
    start_time = datetime.datetime.now()

    #consumer key, consumer secret, access key, access secret.
    args  = parse_args()
    start_stream(args.config_file, start_time)

if __name__ == "__main__":
    main()
