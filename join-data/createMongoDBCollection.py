import json
import pymongo;
from pymongo import MongoClient

# To read data from json
def loadData(filePath):
    data=[]
    with open(filePath) as data_file:
        for document in data_file:
            data.append(json.loads(document))
    return data

# To create dictionary
def creatDict(data , key):
    dict = {}
    for obj in data:
        dict[obj[key]] =obj
    return dict

business_data_path = "/Users/arpitkhandelwal/Downloads/yelp_dataset_challenge_academic_dataset/business.json"
review_data_path = "/Users/arpitkhandelwal/Downloads/yelp_dataset_challenge_academic_dataset/review.json"

client = MongoClient('mongodb://localhost:27017/')
pymongo.unicode_decode_output = False
db = client.yelp_data

business_data = loadData(business_data_path)
print "Loaded business_data"

businessDict = creatDict(business_data , "business_id")
print "Created Business Dicitonary"

review_data = loadData(review_data_path)
print "Loaded review_data"

for x in review_data:
    y = [x["text"],x["business_id"],businessDict[x["business_id"]]["categories"], businessDict[x["business_id"]]["attributes"]]
    s = { 'business_id' : y[1], 'text' : y[0] , 'categories': y[2],'attributes' :y[3]}
    db.review_business_data.insert(s)
print "Data Inserted Successfully"
