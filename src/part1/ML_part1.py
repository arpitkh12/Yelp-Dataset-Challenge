import pymongo
import pandas as pd
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import f1_score
from sklearn.metrics import jaccard_similarity_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.utils import shuffle
from sklearn.linear_model import Perceptron

__author__ = 'arpitkhandelwal'

# MongoDb Connection
client = MongoClient()
db = client.yelp_data
collection = db.review_business_data

# Fetch Data from MongoDB
data = pd.DataFrame(list(collection.find()))

print "Data Loaded from mongodb"
# Preprocessing of data
stopset = set(stopwords.words('english'))
vectorizer = TfidfVectorizer(use_idf=True , lowercase=True, stop_words=stopset)
vectorizer2 = TfidfVectorizer(use_idf=True , lowercase=True, stop_words=stopset,ngram_range=(2, 2))
vectorizer3 = TfidfVectorizer(use_idf=True , lowercase=True, stop_words=stopset,ngram_range=(3, 3))

print "Created TF-idf vectors"
X = data.text

y = data.categories
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(y)

X, y =  shuffle(X, y)
print "Created MultiLabelBinarizer"

X_train,X_test,y_train,y_test = train_test_split(vectorizer.fit_transform(X),y,test_size=0.2,random_state=42)
X_train2,X_test2,y_train2,y_test2 = train_test_split(vectorizer2.fit_transform(X),y,test_size=0.2,random_state=42)
X_train3,X_test3,y_train3,y_test3 = train_test_split(vectorizer3.fit_transform(X),y,test_size=0.2,random_state=42)
classifiers = {"LinearSVC":LinearSVC(), "BernoulliNB":MultinomialNB(), "Perceptron":Perceptron(n_iter=50)}


for i in classifiers.keys():
    clf = MultiOutputClassifier(classifiers[i]).fit(X_train, y_train)

    clf2 = MultiOutputClassifier(classifiers[i]).fit(X_train2, y_train2)
    clf3 = MultiOutputClassifier(classifiers[i]).fit(X_train3, y_train3)
    
    yhat = clf.predict(X_test)
    yhat2 = clf2.predict(X_test2)
    yhat3 = clf3.predict(X_test3)
    
    
    print i, "unigram"
    print "f1_score",f1_score(y_test,yhat,average='samples')
    print "jaccard_similarity_score",jaccard_similarity_score(y_test,yhat)
    print "accuracy_score",accuracy_score(y_test,yhat)
    print "precision_score",precision_score(y_test,yhat,average='samples')
    print "recall_score",recall_score(y_test,yhat,average='samples')
    print "********"
    
    print i, "bigram"
    print "f1_score",f1_score(y_test2,yhat2,average='samples')
    print "jaccard_similarity_score",jaccard_similarity_score(y_test2,yhat2)
    print "accuracy_score",accuracy_score(y_test2,yhat2)
    print "precision_score",precision_score(y_test2,yhat2,average='samples')
    print "recall_score",recall_score(y_test2,yhat2,average='samples')
    print "********"

    print i, "trigram"
    print "f1_score",f1_score(y_test3,yhat3,average='samples')
    print "jaccard_similarity_score",jaccard_similarity_score(y_test3,yhat3)
    print "accuracy_score",accuracy_score(y_test3,yhat3)
    print "precision_score",precision_score(y_test3,yhat3,average='samples')
    print "recall_score",recall_score(y_test3,yhat3,average='samples')
    print "********"

