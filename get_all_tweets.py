import yaml
import argparse
import pandas as pd
from tqdm import tqdm
from pymongo import MongoClient

# DB connector
def mongo_connect(server_name: str) -> MongoClient:
    """Creates connection to the MongoDB database with given server name."""
    client = MongoClient(server_name)
    db = client.twitter_db
    return db

# Credential loader
def load_db_credentials(file_path: str) -> (str, str):
    """Loads username and password from YAML file."""
    with open(file_path) as f:
        key_data = yaml.safe_load(f)
        username = key_data['mongo-db']['username']
        passwd = key_data['mongo-db']['passwd']
    return (username, passwd)

parser = argparse.ArgumentParser(description='Download all the gathered Tweets and save them as a .csv file.')
parser.add_argument('file_name', metavar='FILE',
                    help='File name')

if __name__ == "__main__":
    args = parser.parse_args()

    file_name = args.file_name

    username, passwd = load_db_credentials('auth/read_only.yaml')

    # Connect user to MongoDB database
    db = mongo_connect(f"mongodb+srv://{username}:{passwd}@tweetdb.kpcmn.mongodb.net/<dbname>?retryWrites=true&w=majority")

    # Dataframe for all Tweets
    df_tweets = pd.DataFrame(columns=['_id',
                                    'tweet_text',
                                    'username',
                                    'created_at'])

    # List of archetypes
    #TODO: Migrate list to single file
    archetype_list = ['artist',
                    'caregiver',
                    'everyman',
                    'explorer',
                    'guru',
                    'hero',
                    'innocent',
                    'jester',
                    'magician',
                    'rebel',
                    'ruler',
                    'seducer']

    # Get all tweets from the database
    for archetype in tqdm(archetype_list):
        # Create a cursor for acquiring all posts from the collection
        cursor = db[archetype].find()
        
        df_archetype = pd.DataFrame(list(cursor))
        df_archetype['archetype'] = archetype
        df_tweets = df_tweets.append(df_archetype, ignore_index=True)

    df_tweets.to_csv(file_name)
    print(f"Saved DataFrame as {file_name}")

