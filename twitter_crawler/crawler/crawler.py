import pandas as pd
import yaml
import json
import requests
import sys
import urllib.parse
from typing import TypeVar, Type

sys.path.append(".")
T = TypeVar('T')

from twitter_objects import TweetQuery
from tweepy_functions import tweepy_connect, tweepy_get_tweets
from mongodb_conn.connect_mongo import mongo_connect, mongo_insert


def read_auth() -> str:
    with open("../auth/my_keys.yaml") as f:
        key_data = yaml.safe_load(f)
        bearer_token = key_data['the-tweet-catcher']['bearer-token']
    return bearer_token


def get_attr_list(obj: Type[T]):
    return [a for a in dir(obj) if not a.startswith('__') and not a.startswith('_')]


def create_url(query: TweetQuery):
    # Create attribute list of TweetQuery
    base_query = ''
    attr_list = get_attr_list(query)
    for attribute in attr_list:
        attr_value = getattr(query, attribute)
        if attr_value is not None and len(base_query) == 0:
            base_query += (str(attr_value))
        elif attr_value is not None and len(base_query) > 0:
            base_query += (' ' + str(attr_value))
    base_query += ' lang:en'
    parsed_query = urllib.parse.quote(base_query)

    url = (f'https://api.twitter.com/2/tweets/search/recent?query={parsed_query}'
           f'&max_results={urllib.parse.quote(str(query.max_results))}'
           '&tweet.fields=author_id,created_at,lang,conversation_id'
           '&expansions=author_id,referenced_tweets.id'
           )
    print(url)
    return url


def create_headers(bearer_token: str):
    return {'Authorization': f'Bearer {bearer_token}'}


def connect_to_endpoint(url: str, headers: dict):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_tweets(username_query: str, max_result_count: int = 10, next_token: str = None):
    bearer_token = read_auth()
    headers = create_headers(bearer_token)

    # Create query
    query = TweetQuery()
    query.author_username = username_query
    # query.text_query = username_query
    query.max_results = int(max_result_count)
    full_url = create_url(query)
    if next_token is not None:
        full_url += '&next_token=' + str(next_token)
    json_response = connect_to_endpoint(full_url, headers)
    return json_response


def process_tweets(json_file):
    tweet_list = pd.DataFrame(columns=["username", "text", "created_at"])
    if json_file["meta"]["result_count"] == 0:
        pass
    else:
        data_part = pd.DataFrame(json_file["data"])
        #data_part = pd.DataFrame(json_file["includes"]["tweets"])
        user_part = pd.DataFrame(json_file["includes"]["users"])
        user_part = user_part.rename(columns={"id": "author_id"})
        #username = pd.unique(user_part["username"])[0]
        df_inner = pd.merge(data_part, user_part, on='author_id', how='inner')
        tweet_list = pd.concat([df_inner["username"], df_inner["text"], df_inner["created_at"]], axis=1)
        #tweet_list["text"] = data_part["text"]
        #tweet_list["created_at"] = data_part["created_at"]
        #tweet_list["username"] = username
    return tweet_list

def tweet_to_dict(json_file):
    formatted_tweets = []
    if json_file["meta"]["result_count"] == 0:
        pass
    else:
        data_part = pd.DataFrame(json_file["data"])
        user_part = pd.DataFrame(json_file["includes"]["users"])
        user_part = user_part.rename(columns={"id": "author_id"})
        df_inner = pd.merge(data_part, user_part, on='author_id', how='inner')
        tweet_list = pd.concat([df_inner["username"], df_inner["text"], df_inner["created_at"]], axis=1)
        for i in range(len(tweet_list)):
            formatted_tweets.append({
                'tweet_text':tweet_list["text"][i],
                'username': df_inner["username"][i],
                'created_at': df_inner["created_at"][i]
            })
    return formatted_tweets


def crawl_twitter(username_to_query:str, max_result_count: int):
    tweet_base = pd.DataFrame(columns=["username", "text", "created_at"])
    data = get_tweets(username_query=username_to_query, max_result_count=10)
    while True:
        tweet_list_req = process_tweets(data)
        if tweet_list_req.shape[0] <= 0:
            break
        else:
            tweet_base = tweet_base.append(tweet_list_req, ignore_index=True)
            if ("next_token" not in data["meta"].keys()) or tweet_base.shape[0] > max_result_count:
                break
            next_token_str = data["meta"]["next_token"]
            data = get_tweets(username_query=username_to_query, max_result_count=10, next_token=next_token_str)
    return tweet_base

def crawl_twitter_mongo(username_to_query:str, max_result_count: int, db, collection_name: str):
    data = get_tweets(username_query=username_to_query, max_result_count=max_result_count)
    tweet_count = 0
    while True:
        tweet_list = tweet_to_dict(data)
        tweet_count += len(tweet_list)
        if len(tweet_list) <= 0:
            break
        else:
            mongo_insert(db, tweet_list, collection_name=collection_name)
            if ("next_token" not in data["meta"].keys()) or tweet_count >= max_result_count:
                break
            next_token_str = data["meta"]["next_token"]
            data = get_tweets(username_query=username_to_query, max_result_count=10, next_token=next_token_str)
    return tweet_count

def crawl_twitter_tweepy(username_to_query:str, max_result_count: int, db, api, collection_name: str):
    tweet_list = []
    try:
        tweet_list = tweepy_get_tweets(api, username_to_query, max_result_count)
    except Exception as e:
        pass
    finally:
        if len(tweet_list) > 0:
            mongo_insert(db, tweet_list, collection_name=collection_name)
        else:
            pass
    return len(tweet_list)


if __name__ == "__main__":
    file_name = "seducer"
    path_file = f'../../archetype_lists/{file_name}.txt'
    with open(path_file, 'r') as f:
        user_list = f.readlines()
    db = mongo_connect('localhost')
    api = tweepy_connect("../auth/my_keys.yaml")
    for user in user_list:
        tweets_acquired = crawl_twitter_tweepy(user, 100, db, api, file_name)
        if tweets_acquired > 0:
            print(f'Number of acquired tweets for user {user}: {tweets_acquired}')
        else:
            print(f'No tweets acquired. Closing crawler for user {user}')
