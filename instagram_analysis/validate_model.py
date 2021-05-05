# Script for validating the created models

# Dependencies
import pandas as pd
import numpy as np
from tqdm import tqdm
import copy
import os
import toml
import re
import itertools
from text_cleaner import *
import operator
from collections import Counter
import pickle

def extract_hashtags(post_text):
    HASH_RE = re.compile(r"\#\w+")
    out_list = re.findall(HASH_RE, post_text)
    return out_list

arch_df = pd.read_csv('archetypes_pl.csv', index_col=0)

# Save the order of columns
trait_list = arch_df.columns.tolist()

# Show the table header and column list
print(trait_list)
arch_df.head()

# Table preprocessing - replace all NaN with 2 (Unrelated/Don't know class), replace 0-5 values with the ones in range -1.0 - 1.0
arch_df = arch_df.fillna(2.0)

arch_df = arch_df.replace(0.0, -1.0)
arch_df = arch_df.replace(1.0, -0.5)
arch_df = arch_df.replace(2.0, 0.0)
arch_df = arch_df.replace(3.0, 0.5)
arch_df = arch_df.replace(4.0, 1.0)

# Remove duplicated annotations, to exclude conflicting entries
arch_df = arch_df[~arch_df.index.duplicated(keep='first')]

# Print the head of the dataset after modification
arch_df.head()

# Check if a user has a non-empty directory in the dataset, otherwise delete the user from the list
available_arch_df = copy.deepcopy(arch_df)
posts = []

BASE_DIR = "instagram_dataset/pl"

# Iterate over whole DataFrame
for i, row in tqdm(arch_df.iterrows()):
    profile_posts = []
    profile_hashtags = []
    
    # Iterate over all categories in base directory
    for cat_dir in os.listdir(BASE_DIR):
        whole_cat_dir = os.path.join(BASE_DIR, cat_dir)
        
        # If profile exists in the database
        if i in os.listdir(whole_cat_dir):
            profile_path = os.path.join(whole_cat_dir, i)
            profile_config_path = os.path.join(whole_cat_dir, i, f"{i}.toml")
            
            # Check if there's a .toml file - if not, omit the profile
            is_present = False            
            if os.path.exists(profile_config_path):
                is_present = True
                for file in os.listdir(profile_path):
                    if not file.endswith(".toml"):
                        with open(os.path.join(profile_path, file), "r") as post_f:
                            read_text = post_f.read()
                            profile_posts.append(remove_stopwords(clean_up_text(read_text)))
                            profile_hashtags.append(extract_hashtags(read_text))
            else:
                available_arch_df = available_arch_df.drop(i, axis=0)
                print(f"Profile {i} has no posts.")
            # Create new list for a given user    
            if is_present:
                # Merge lists - a single list for a single influencer
                profile_hashtags = list(itertools.chain.from_iterable(profile_hashtags))
                posts.append(list(itertools.chain.from_iterable([profile_posts, [profile_hashtags]])))
            break

users = list(available_arch_df.index.values)
user_indices = {k: users.index(k) for k in users}

# Load the required pickles
with open("word_frequency_table.pickle", "rb") as f:
    word_df = pickle.load(f)

# Word map - to easily create output vectors
word_map = word_df.columns.tolist()

def get_trait_dot_product(post_text: str, word_map: list, word_dataframe: pd.DataFrame) -> list:
    # Filter out the text
    filtered_post = remove_stopwords(clean_up_text(post_text))
    filtered_post += extract_hashtags(post_text)
    
    # Create a vector for dot product vector
    post_vector = [0] * len(word_map)
    
    # Calculate word occurrences
    word_ctr = Counter(filtered_post)
    
    for word, freq in word_ctr.items():
        if word in word_map:
            post_vector[word_map.index(word)] = freq
    
    # Calculate dot product for a given text
    word_dot = word_dataframe.dot(post_vector)
    return word_dot.tolist()

# Replace NaN with 0 in word_frequency_table
word_df = word_df.fillna(0)

# Method for calculating the dot product of trait <-> influencer relation
def get_influencer_dot_product(trait_output: list, influencer_dataframe: pd.DataFrame) -> pd.DataFrame:
    return influencer_dataframe.dot(trait_output)

# Method for calculating the similarity
def calculate_similarity(post_text: str, 
                         word_map: list, 
                         word_dataframe: pd.DataFrame,
                         influencer_dataframe: pd.DataFrame) -> pd.DataFrame:
    # Calculate word-trait dot product
    post_result = get_trait_dot_product(post_text, word_map, word_dataframe)
    print(f"Post result: {post_result}")
    
    # Calculate trate-influencer dot-product
    return get_influencer_dot_product(post_result, influencer_dataframe)

pbar = tqdm(available_arch_df.iterrows())
accuracy = 0.0

for idx, row in pbar:
    user_text = list(itertools.chain.from_iterable(posts[users.index(idx)]))
    user_text = " ".join(user_text)
    sim_df = calculate_similarity(user_text, word_map, word_df, available_arch_df)
    if idx == sim_df.idxmax():
        accuracy += 1.
    print(f"Predicted: {sim_df.idxmax()}, real: {idx}")
    print(sim_df)
    input("Waiting...")  
    pbar.set_description(f"Current accuracy: {round(accuracy / len(available_arch_df), 2)}")