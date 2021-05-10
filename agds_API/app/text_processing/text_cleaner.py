import re
import nltk
import pandas as pd
from nltk.corpus import stopwords

# Stopwords object
with open("text_processing/polish_stopwords.txt", "r") as f:
    stop_words = f.read().strip("\n")

# Regular expressions used for the text cleaning
URL_PATTERN = re.compile(r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)")
USERNAME_PATTERN = re.compile('@[^\s]+')
HASH_PATTERN = re.compile(r"\#\w+")
ALPHA_PATTERN = re.compile("[^a-zA-ZąćęłńóśźżĄĘŁŃÓŚŹŻ]")
LONG_SEQ_PATTERN = re.compile(r"(.)\1\1+")
REPL_SEQ_PATTERN = r"\1\1"

def clean_up_text(tweet: str) -> str:
    """Cleans up the Tweet's text from emojis, usernames, links, etc."""
    lc_tweet = tweet.lower()
    
    # Remove unnecessary characters
    lc_tweet = re.sub(URL_PATTERN, '', lc_tweet)
    lc_tweet = re.sub(USERNAME_PATTERN, '', lc_tweet)
    lc_tweet = re.sub(HASH_PATTERN, '', lc_tweet)
    lc_tweet = re.sub(ALPHA_PATTERN, ' ', lc_tweet)
    lc_tweet = re.sub(LONG_SEQ_PATTERN, REPL_SEQ_PATTERN, lc_tweet)
    lc_tweet = re.sub(' +', ' ', lc_tweet)
    lc_tweet = lc_tweet.lstrip(" ").rstrip(" ")
    lc_tweet = nltk.word_tokenize(lc_tweet)

    return lc_tweet    

def remove_stopwords(word_list: list) -> list:
    """Removes the stopwords from the tokenized tweet."""
    out_list = []
    for word in word_list:
        if word not in stop_words:
            out_list.append(word)
            
    return out_list