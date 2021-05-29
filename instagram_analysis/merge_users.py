import os
import glob
import pandas as pd
from distutils.dir_util import copy_tree
from tqdm import tqdm

DATA_DIR = 'instagram_dataset/pl'
OUT_DIR = 'instagram_cleared'

# Read the .csv file
old_influencer_df = pd.read_csv('archetypes_pl.csv', index_col=0)
influencer_df = pd.read_csv('archetypes_pl_new.csv', index_col=0)
influencer_df = influencer_df[~influencer_df.index.duplicated(keep='first')]

cols = old_influencer_df.columns.tolist()
print(f"Column order: {cols}")
cont = input("Continue? [y/n]")
if cont == "y":
    new_influencer_df = pd.DataFrame(columns=cols)

    user_list = list(influencer_df.index.values)
    new_users = 0
    for user in tqdm(user_list):
        new_dir = f"{OUT_DIR}/{user}"
        if os.path.isdir(new_dir):
            continue
        os.mkdir(new_dir)
        dir_list = glob.glob(f"{DATA_DIR}/*/{user}")
        for directory in dir_list:
            copy_tree(directory, new_dir)
        new_users += 1
        new_influencer_df = new_influencer_df.append(influencer_df.loc[user])

    print(f"New user count: {new_users}")
    new_influencer_df.to_csv("test_archetypes_pl.csv")
