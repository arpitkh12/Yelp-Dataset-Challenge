import pymongo;
from pymongo import MongoClient
import csv, json,ast

# client = MongoClient()
# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://localhost:27017/')
pymongo.unicode_decode_output = False
db = client.yelp_data
collection_review = db.review_data
collection_tip = db.tip_data
collection_business = db.business_data
cursor_review = collection_review.find({},{"text":1 , "business_id":1})
# cursor_tip = collection_tip.find({},{"text":1 , "business_id":1})
data_review_category=[]

count =0;

# To map review with category
for   data in cursor_review:
#    count+=1;
    y = collection_business.find_one({"business_id":data[u'business_id']}, {"categories":1})
    data_review_category.append((data[u'text'],y[u'categories']))
#    if count%10000 == 0:
#        print "Hello"
#    if count== 100000:
#        break;
myfile = open("data2.csv", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
for row in ast.literal_eval(json.dumps(data_review_category)):
    wr.writerow(row)
    myfile.flush()
myfile.close()
