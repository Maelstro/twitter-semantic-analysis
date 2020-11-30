import  argparse
from twitter_crawler.crawler.crawler import scrape_tweets
import sys
sys.path.append(".")

parser = argparse.ArgumentParser()
parser.add_argument("list_name", type=str)
parser.add_argument("dir_path", type=str)
parser.add_argument("auth_path", type=str)
args = parser.parse_args()


list_name = str(args.list_name)
dir_path = str(args.dir_path)
auth_path = str(args.auth_path)
scrape_tweets(list_name, dir_path, auth_path)
