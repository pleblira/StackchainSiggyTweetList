import sqlite3
import random
import boto3
from dotenv import load_dotenv, find_dotenv
import os
import json

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


# cursor = connection.execute('select * from main_item')
# names = list(map(lambda x: x[0], cursor.description))
# print(f"the column names for the tweets table are: {names}")
# print(names[3])


# prints all tables in db
# print(cursor.fetchall())

def update_s3(tweet_type):
  connection = sqlite3.connect('db.sqlite3')
  sql_query = "SELECT name FROM sqlite_master WHERE type='table'"
  cursor = connection.cursor()
  cursor.execute(sql_query)
  if tweet_type == "stackchain":
    tweet_type_column_number = 25
    tweets_json_file_location = "tweetlist_jsons/stackchain.json"
  elif tweet_type == "stackchaintip":
    tweet_type_column_number = 26
    tweets_json_file_location = "tweetlist_jsons/stackchaintip.json"
  elif tweet_type == "pbstack":
    tweet_type_column_number = 28
    tweets_json_file_location = "tweetlist_jsons/pbstack.json"
  else:
    tweet_type_column_number = 27
    tweets_json_file_location = "tweetlist_jsons/stackjoin.json"
  cursor.execute("SELECT * FROM " + "main_item")
  rows = cursor.fetchall()

  # appending tweet list to json file
  with open(tweets_json_file_location, 'w') as openfile:
    try:
        tweet_list = json.load(openfile)
        print("working")
    except:
        tweet_list = []
        print("excepting")
        # json.dump(tweet_list, filename)
    for row in rows:
      if row[3] == tweet_type_column_number:
        tweet_list.append({"tweet_id":row[0],"tweet_text":row[1]})
    openfile.seek(0)
    openfile.write(json.dumps(tweet_list, indent=4))

    # overwriting tweet list file back to S3
    s3_upload = boto3.resource(
        's3',
        region_name='us-east-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    content=json.dumps(tweet_list).encode('utf-8')
    s3_upload.Object('pleblira', tweets_json_file_location.replace("tweetlist_jsons/","")).put(Body=content,ACL="public-read")


# def print_all_items(table, tweet_type):
#   if tweet_type == "#stackchain":
#     tweet_type_column_number = 25
#   elif tweet_type == "#stackchaintip":
#     tweet_type_column_number = 26
#   else:
#     tweet_type_column_number = 27
#   tweet_list_to_choose_at_random = []
#   cursor.execute("SELECT * FROM " + table)
#   rows = cursor.fetchall()
#   for row in rows:
#     if row[3] == tweet_type_column_number:
#       print(row[1] + "\n\n")
#       tweet_list_to_choose_at_random.append(row[0])
#   print(tweet_list_to_choose_at_random)
#   randomly_selected_tweet = random.choice(tweet_list_to_choose_at_random)
#   for row in rows:
#     if row[0] == randomly_selected_tweet:
#       print(row[1])



# print_all_items('main_item', "#stackchaintip")

# if __name__ == '__main__':
#     update_s3("stackchain")

