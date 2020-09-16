from pymongo import MongoClient

client = MongoClient('172.104.190.208', username='arynas',  password='Arynas92')
db = client.sinta
col_google_scholars = db.google_scholars

print(list(col_google_scholars.find().sort('_id', -1).limit(1)))

# ids = [data['_id'] for data in col_google_scholars.find().sort('_id', -1).limit(1273)]
#
# col_google_scholars.remove({'_id': {'$in': ids}})