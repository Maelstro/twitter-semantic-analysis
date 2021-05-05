import os
import glob
import pandas as pd
from distutils.dir_util import copy_tree

DATA_DIR = 'instagram_dataset/pl'
OUT_DIR = 'instagram_cleared'

# Read the .csv file
influencer_df = pd.read_csv('archetypes_pl.csv', index_col=0)
influencer_df = influencer_df[~influencer_df.index.duplicated(keep='first')]


user_list = list(influencer_df.index.values)
for user in user_list:
    new_dir = f"{OUT_DIR}/{user}"
    os.mkdir(new_dir)
    dir_list = glob.glob(f"{DATA_DIR}/*/{user}")
    for directory in dir_list:
        copy_tree(directory, new_dir)
