from pymongo import MongoClient

client = MongoClient('YOURHOST', username='YOURUSERNAME',  password='YOURPASSWORD')
db = client.sinta
col_google_scholars = db.google_scholars

print(list(col_google_scholars.find().sort('_id', -1).limit(1)))
