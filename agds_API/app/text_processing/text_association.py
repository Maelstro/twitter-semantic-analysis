# text_association.py - calculates the similarity between the text and the influencers

import pandas as pd
from .text_cleaner import *
import re
from collections import Counter
import numpy as np
import pickle

class TextProcessor(object):
    def __init__(self):
        # Load the required files
        with open("text_processing/word_map_non_negative.pickle", "rb") as f:
            self.word_map = pickle.load(f)

        with open("text_processing/word_trait_array_non_negative.pickle", "rb") as f:
            self.word_df = pickle.load(f)
        self.arch_df = pd.read_csv("text_processing/influencer_recalc.csv", header=0, index_col=0)

    def extract_hashtags(self, post_text):
        HASH_RE = re.compile(r"\#\w+")
        out_list = re.findall(HASH_RE, post_text)
        return out_list

    def get_trait_dot_product(self, post_text: str) -> list:
        # Filter out the text
        filtered_post = remove_stopwords(clean_up_text(post_text))
        filtered_post += self.extract_hashtags(post_text)

        # Create a vector for dot product vector
        post_vector = [0] * len(self.word_map)

        # Calculate word occurrences
        word_ctr = Counter(filtered_post)

        for word, freq in word_ctr.items():
            if word in self.word_map:
                post_vector[self.word_map.index(word)] = freq

        # Calculate dot product for a given text
        word_dot = self.word_df.dot(post_vector)
        return word_dot

    # Method for calculating the similarity
    def calculate_similarity(self, post_text: str) -> (pd.Series, pd.Series):
        # Calculate word-trait dot product
        post_result = self.get_trait_dot_product(post_text)

        # Generate new dataframe - one row per influencer
        inf_df = pd.Series(index=self.arch_df.index)

        # Replace all data in temporary df with calculated post result
        for idx in inf_df.index:
            inf_df.loc[idx] = np.linalg.norm(self.arch_df.loc[idx] - post_result)

        return post_result, inf_df.sort_values()