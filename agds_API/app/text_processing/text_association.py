# text_association.py - calculates the similarity between the text and the influencers

import pandas as pd
from .text_cleaner import *
import re
from collections import Counter
import numpy as np
import pickle
from scipy.special import softmax
import tensorflow as tf

class TextProcessor(object):
    def __init__(self):
        # Load the required files
        with open("text_processing/finetuned_s90_10_word_trait_array.pickle", "rb") as f:
            self.word_df = pickle.load(f)

        # Generate word map from AGDS
        self.word_map = self.word_df.columns.tolist()

        # Read archetype list and clean it up
        self.arch_df = pd.read_csv("text_processing/archetypes_pl_new.csv", header=0, index_col=0)
        self.arch_df = self.arch_df.fillna(2)
        self.arch_df = self.arch_df[~self.arch_df.index.duplicated(keep='first')]

        # Generate trait list
        self.trait_list = self.arch_df.columns.tolist()

        # Load LSTM model
        self.test_model = tf.keras.models.load_model("text_processing/nn_model")


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

        out_vec = pd.Series()
        for trait in self.trait_list:
            out_vec = out_vec.append(pd.Series([np.argmax(softmax(word_dot.loc[trait]))], index=[trait]))

        return out_vec

    # Trait accuracy - round the results
    def natural_round(x: float) -> int:
        out = int(x // 1)
        return out + 1 if (x - out) >= 0.5 else out

    def accuracy_per_trait(input_vector: pd.Series, annotated_vector: pd.Series) -> np.array:
        out_array = np.array([0] * 37, dtype=np.int)
        for i in range(len(out_array)):
            if input_vector[i] == annotated_vector[i]:
                out_array[i] = 1
        return out_array

    # Method for calculating the similarity
    def calculate_similarity(self, post_text: str) -> (pd.Series, pd.Series):
        # Calculate word-trait dot product
        post_result = self.get_trait_dot_product(post_text)

        # Generate new dataframe - one row per influencer
        inf_df = pd.Series(index=self.arch_df.index)

        # Replace all data in temporary df with calculated post result
        for idx in inf_df.index:
            inf_df.loc[idx] = np.linalg.norm(self.arch_df.loc[idx] - post_result)

        sorted_infs = inf_df.sort_values()
        return post_result, sorted_infs

    def clean_post(self, src_text: str) -> str:
        # Extract posts and hashtags
        extracted_text = remove_stopwords(clean_up_text(src_text))
        extracted_hashtags = self.extract_hashtags(src_text)
        return extracted_text + extracted_hashtags

    def predict_nn(self, post_text):
        # Preprocess the text
        user_text = " ".join(self.clean_post(post_text))

        # Make a prediction
        prediction = self.test_model.predict([user_text])

        # Process the predictions
        predicted_classes = []
        for trait in prediction:
            predicted_classes.append(int(np.argmax(trait)))

        predicted_dict = {trait: pred for trait, pred in zip(self.trait_list, predicted_classes)}
        series_pred = pd.Series(predicted_dict)

        return series_pred

    def nn_similarity(self, predicted_classes):
        # Generate new dataframe - one row per influencer
        inf_df = pd.Series(index=self.arch_df.index)

        # Replace all data in temporary df with calculated post result
        for idx in inf_df.index:
            inf_df.loc[idx] = np.linalg.norm(self.arch_df.loc[idx] - predicted_classes)

        sorted_infs = inf_df.sort_values()
        return sorted_infs