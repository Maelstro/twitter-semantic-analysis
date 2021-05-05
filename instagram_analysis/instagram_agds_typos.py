# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Instagram data analysis
import pandas as pd
from tqdm import tqdm


# %%
# Read the .csv with annotated data
arch_df = pd.read_csv('archetypes_pl.csv', index_col=0)

# Get the DataFrame description
arch_df.describe()


# %%
# Print the head of the dataset
arch_df.head()


# %%
# Fill NaN values with Unrelated/Don't Know class
arch_df = arch_df.fillna(2.0)

# Replace values: 0 is -1, 1 is -0.5, 2 is 0.0, 3 is 0.5, 4 is 1.0
arch_df = arch_df.replace(0.0, -1.0)
arch_df = arch_df.replace(1.0, -0.5)
arch_df = arch_df.replace(2.0, 0.0)
arch_df = arch_df.replace(3.0, 0.5)
arch_df = arch_df.replace(4.0, 1.0)
arch_df = arch_df[~arch_df.index.duplicated(keep='first')]


# Print the head of the dataset after modification
arch_df.head()


# %%
print(arch_df.loc["marek_grodzki"].to_dict())


# %%
# InfluencerNode - node with user data

import os
import toml
import re
import itertools
from text_cleaner import *

class InfluencerNode(object):
    def __init__(self, profile_name: str, db_directory: str, data_frame: pd.DataFrame):
        self.username = profile_name

        # Load the user data
        try:
            if os.path.exists(db_directory):
                # Iterate over directories in categories:
                category_dirs = os.listdir(db_directory)
                for cat_dir in category_dirs:
                    user_dir = os.path.join(db_directory, cat_dir)
                    # Check if influencer username is present in this category
                    if profile_name in os.listdir(user_dir):
                        user_path = os.path.join(user_dir, profile_name)
                        # Get user data
                        with open(os.path.join(user_path, f"{profile_name}.toml"), "r") as f:
                            toml_file = toml.load(f)
                        
                        # After reading .toml file, set up the node attributes
                        self.full_name: str = toml_file["full_name"]
                        self.biography: str = toml_file["biography"]
                        self.business_category: str = toml_file["business_category_name"]
                        self.followers: int = toml_file["followers"]
                        self.followees: int = toml_file["followees"]
                        self.mediacount: int = toml_file["mediacount"]
                        self.posts: list = []

                        # Red all posts into a list
                        for file in os.listdir(user_path):
                            if not file.endswith(".toml"):
                                with open(os.path.join(user_path, file), "r") as post_f:
                                    self.posts.append(post_f.read())

                        self.hashtags = self.extract_hashtags()

                        # Post reedition
                        self.posts = [remove_stopwords(clean_up_text(post)) for post in self.posts]
                        
                        # Set up archetype/character trait weights
                        traits = data_frame.loc[self.username].to_dict()
                        for k, v in traits.items():
                            setattr(self, k, v)

        except FileNotFoundError as e:
            print(e)

    def extract_hashtags(self):
        HASH_RE = re.compile(r"\#\w+")
        out_list = []
        for post in self.posts:
            tmp = re.findall(HASH_RE, post)
            out_list.append(list(set(tmp)))
        out_list = list(itertools.chain.from_iterable(out_list))
        return list(set(out_list))
            


# %%
# Test the class
test_user = InfluencerNode("marek_grodzki", "instagram_dataset/pl", arch_df)

# Print the hashtags associated with the user
print(test_user.hashtags)


# %%
# Create node list (to be used for graph building)
import copy
node_list = []
data_not_present = []
available_arch_df = copy.deepcopy(arch_df)

for i, row in tqdm(arch_df.iterrows()):
    try:
        tmp = InfluencerNode(i, "instagram_dataset/pl", arch_df)
        node_list.append(tmp)
    except:
        available_arch_df.drop(i, axis=0, inplace=True)


# %%
# Get the length of the processed node list
print(f"Node list length: {len(available_arch_df)}")


# %%
from collections import Counter
import itertools

def select_and_aggregate_per_trait(data_frame: pd.DataFrame):
    # Select only the accounts assigned with the given trait
    word_df = pd.DataFrame()
    for col in tqdm(arch_df.columns):
        out_df = data_frame[data_frame[col] != 0.0]
        trait_posts = []
        total_ctr = Counter()
        for i, row in out_df.iterrows():
            # Get the needed posts and hashtags
            trait_posts += (list(itertools.chain.from_iterable(node_list[out_df.index.get_loc(i)].posts)) + node_list[out_df.index.get_loc(i)].hashtags) 

            # Get count of all words
            tmp_ctr = Counter(trait_posts)
            total_ctr += Counter(trait_posts)
            word_df = pd.concat([word_df, pd.DataFrame.from_dict(total_ctr, orient="index", columns=[col])])
    return word_df


# %%



# %%
word_df = select_and_aggregate_per_trait(available_arch_df)


# %%
# Save the DataFrame as a pickle
import pickle
with open("word_df.pickle", "wb") as f:
    pickle.dump(word_df, f)


