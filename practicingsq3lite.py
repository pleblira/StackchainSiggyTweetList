import sqlite3
import random

connection = sqlite3.connect('db.sqlite3')

cursor = connection.execute('select * from main_item')
names = list(map(lambda x: x[0], cursor.description))
print(f"the column names for the tweets table are: {names}")
print(names[3])

sql_query = "SELECT name FROM sqlite_master WHERE type='table'"
cursor = connection.cursor()
cursor = connection.cursor()
cursor.execute(sql_query)

# prints all tables in db
print(cursor.fetchall())

def print_all_items(table, tweet_type):
  if tweet_type == "#stackchain":
    tweet_type_column_number = 25
  elif tweet_type == "#stackchaintip":
    tweet_type_column_number = 26
  else:
    tweet_type_column_number = 27
  tweet_list_to_choose_at_random = []
  cursor.execute("SELECT * FROM " + table)
  rows = cursor.fetchall()
  for row in rows:
    if row[3] == tweet_type_column_number:
      print(row[1] + "\n\n")
      tweet_list_to_choose_at_random.append(row[0])
  print(tweet_list_to_choose_at_random)
  randomly_selected_tweet = random.choice(tweet_list_to_choose_at_random)
  for row in rows:
    if row[0] == randomly_selected_tweet:
      print(row[1])

print_all_items('main_item', "#stackchaintip")

# print_all_items('main_todolist', None)

