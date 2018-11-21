#!/usr/bin/env python
import os
import sys
import ast

import pandas as pd


def hashtag_clean(record):
    try:
        record = ast.literal_eval(record)
        record = [i['text'] for i in record]
    except Exception as e:
        record = record
    return record

def user_mentions_clean(record):
    try:
        record = ast.literal_eval(record)
        record = [(i['screen_name'], i['id']) for i in record]
        record = dict(record)
    except Exception as e:
        record = record
    return record

def url_clean(record):
    try:
        record = ast.literal_eval(record)
        record = [i['expanded_url'] for i in record]
    except Exception as e:
        record = record
    return record

def load_and_clean(file):
    fp = open(file, 'r')
    dtype={'TweetID': str, 'Timestamp': str, 'Full_Text': str, 'In_Reply_To_User_ID': str, 'User_ID': str,
       'User_Name': str, 'User_Screen_Name': str, 'Coordinates': str, 'Place': str, 'Bounding_Box': str,
       'Quoted_Status_ID': str, 'Retweeted_Status': str, 'Hashtags': str, 'URLs': str,
       'User_Mentions': str, 'Media': str, 'Language': str}
    df = pd.read_csv(fp, dtype=dtype, encoding='utf-8')
    #     df = pd.read_csv(fp, dtype=dtype)
    output = os.path.splitext(file)[0] + "_edit.csv"
    print("Loaded", file)

    df['Hashtags'] = df['Hashtags'].apply(hashtag_clean)
    df['User_Mentions'] = df['User_Mentions'].apply(user_mentions_clean)
    df['URLs'] = df['URLs'].apply(url_clean)

    df.to_csv(output, sep="\t")
    print("Cleaned", file)

    fp.close()

if __name__ == '__main__':
    data = sys.stdin.read()
    for file in data.split('\n'):
        try:
            load_and_clean(file)
        except Exception as e:
            print("<======= Unable to clean file:", file, "=======>")
            print(e)
