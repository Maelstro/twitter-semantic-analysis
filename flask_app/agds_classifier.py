import pickle
import itertools
import operator
import pandas as pd
impor


class AGDSClassifier:
    def __init__(self):
        self.AGDS_word_to_tweet: dict = {}
        self.AGDS_tweet_to_archetype: dict = {}
        self.df_tweets = None

    def read_agds_layer(self, word_to_tweet_path: str, tweet_to_archetype: str):
        with open(word_to_tweet_path, "r") as f:
            self.AGDS_word_to_tweet = pickle.load(f)

        with open(word_to_tweet_path, "r") as f:
            self.AGDS_tweet_to_archetype = pickle.load(f)

    def get_jaccard_similarity(self, text_A: str, text_B: str) -> float:
        intersection = len(list(set(text_A).intersection(text_B)))
        union = (len(text_A) + len(text_B)) - intersection
        return float(intersection) / union

    def get_similarity(self, text_to_classify: str):


    def find_nearest_neighbors(self, row, k) -> dict:
        ### PART 1 - associate words with Tweets and get the Jaccard similarity
        similar_tweets = []

        for word in row:
            try:
                similar_tweets.append(self.AGDS_word_to_tweet[word])
            except:
                pass

        similar_tweets = set(itertools.chain.from_iterable(similar_tweets))

        tweet_similarity = []
        for s_tweet in similar_tweets:
            tweet_similarity.append((s_tweet, get_jaccard_similarity(row, tweet_df.iloc[s_tweet].processed_tweet)))
        tweet_similarity = sorted(tweet_similarity, key=lambda x: x[1])
        tweet_similarity = tweet_similarity[-k:]

        ### PART 2 - associate Tweets with archetypes
        similar_archetypes = {}
        similarity_sum = 0

        for pair in tweet_similarity:
            idx, jacc = pair
            similarity_sum += jacc

            if self.tweet_df.iloc[idx].archetype in similar_archetypes:
                similar_archetypes[self.tweet_df.iloc[idx].archetype] += jacc
            else:
                similar_archetypes[tweet_df.iloc[idx].archetype] = jacc

        for key in similar_archetypes.keys():
            similar_archetypes[key] /= similarity_sum

        return similar_archetypes