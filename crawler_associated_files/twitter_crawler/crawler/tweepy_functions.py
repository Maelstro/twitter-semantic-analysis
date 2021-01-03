import tweepy
import yaml

import sys
sys.path.append("")

def tweepy_read_auth(yaml_path) -> (str, str):
    with open(yaml_path) as f:
        key_data = yaml.safe_load(f)
        cons_key = key_data['the-tweet-catcher']['api-key']
        cons_secret = key_data['the-tweet-catcher']['api-secret-key']
    return (cons_key, cons_secret)


def tweepy_connect(yaml_path):
    cons_key, cons_secret = tweepy_read_auth(yaml_path)
    auth = tweepy.AppAuthHandler(cons_key, cons_secret)
    api = tweepy.API(auth)
    return api

def tweepy_get_tweets(api, username:str, max_count: int = 10):
    tweet_list = []
    query = 'from:' + username
    for tweet in tweepy.Cursor(api.search, q=query).items(max_count):
        status = api.get_status(tweet.id, tweet_mode="extended")
        try:
            full_tweet = status.retweeted_status.full_text
        except AttributeError:  # Not a Retweet
            full_tweet = status.full_text
        finally:
            tweet_list.append({
                    'tweet_text':full_tweet,
                    'username': tweet.user.screen_name,
                    'created_at': tweet.created_at
                })
    return tweet_list