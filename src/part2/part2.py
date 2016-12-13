import pymongo
import pandas as pd
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import BernoulliNB
from sklearn import tree
from scipy.sparse import csr_matrix
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.dummy import DummyClassifier
from textblob import TextBlob
from sklearn.decomposition import PCA
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import RidgeClassifier
import csv

import numpy as np
import copy
from sklearn.decomposition import TruncatedSVD
__author__ = 'tejashree'

csv_output=[]
attribute_to_predict = u'Delivery'
word_dict={u'Good for Kids':[u'kid$',u'good for kids', u'kids' , u'child', u'family'],u'Delivery':[u'delivery']}
classifiers = {"LinearSVC":LinearSVC(), "Perceptron":Perceptron(n_iter=50), "BernoulliNB":BernoulliNB(), "RandomForestClassifier":RandomForestClassifier(n_estimators=10)}
y_global = None
def baselineClassification(X_train,X_test,y_train,y_test,i,features):
    clf  =DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
    print "Score for most_frequent"
    yhat = clf.predict(X_test)
    print "confusion matrix:\n", confusion_matrix(y_test, yhat)
    accuracy = accuracy_score(y_test, yhat)
    print "Accuracy:",accuracy
    prf = precision_recall_fscore_support(y_test, yhat,average='weighted')
    print "(precision,recall,fscore,support):",prf
    csv_output.append([i, features, accuracy, prf[0],prf[1],prf[2]])


def trainAndTest(X_train,X_test,y_train,y_test,i,features):
    print i
    clf  = classifiers[i].fit(X_train, y_train)
    yhat = clf.predict(X_test)
    print "confusion matrix:\n", confusion_matrix(y_test, yhat)
    accuracy = accuracy_score(y_test, yhat)
    print "Accuracy:",accuracy
    prf = precision_recall_fscore_support(y_test, yhat,average='weighted')
    print "(precision,recall,fscore,support):",prf
    csv_output.append([i, features, accuracy, prf[0],prf[1],prf[2]])
def getBaseLine(Xinput,yinput,removeStopWords,n1,n2):
    global y_global
    y = [yi[attribute_to_predict] if attribute_to_predict in yi else None for yi in yinput]
    X = [Xinput[i] for i in range(0,len(y)) if y[i] is not None ]
    y = [y[i] for i in range(0,len(y)) if y[i] is not None ]
    print "removed data without required attributes"

    if removeStopWords:
        stopset = set(stopwords.words('english'))
        vectorizer = TfidfVectorizer(use_idf=True , lowercase=True, stop_words=stopset,ngram_range=(n1, n2))
    else:
        vectorizer = TfidfVectorizer(use_idf=True , lowercase=True, ngram_range=(n1, n2))

    X = vectorizer.fit_transform(X)

    print "Created TF-idf vectors"
    if y_global==None:
        le = LabelEncoder()
        y = le.fit_transform(y)
        y_global=y
        print "Encoded Labels"
    else:
        y = y_global
    # Train Test Split
    return train_test_split(X,y,test_size=0.2,random_state=42)

def getSentimentPolarity(Xinput,yinput):
    global y_global
    word = word_dict[attribute_to_predict]
    print word
    y = [yi[attribute_to_predict] if attribute_to_predict in yi else None for yi in yinput]
    Xtext = [Xinput[i] for i in range(0,len(y)) if y[i] is not None ]
    y = [y[i] for i in range(0,len(y)) if y[i] is not None ]
    print "removed data without required attributes"
    X = []
    count = 1
    for i in range(len(Xtext)):
        pure=TextBlob(Xtext[i])
        value = 0
        for sentence in pure.sentences:
            a=sentence
            if any([w in a.lower() for w in word]):
                count+=1
                value = sentence.sentiment.polarity#1 if  pure.sentiment.polarity > 0.2 else -1 #1 if  pure.sentiment.polarity > 0.2 else 2
                break
    
        X.append([value])
    #print X
    if y_global==None:
        le = LabelEncoder()
        y = le.fit_transform(y)
        y_global=y
        print "Encoded Labels"
    else:
        y = y_global
    print "Encoded Labels"
    
    # Train Test Split
    return np.array(train_test_split(X,y,test_size=0.2,random_state=42))

def getCategories(Xinput,yinput,cinput):
    global y_global
    y = [yi[attribute_to_predict] if attribute_to_predict in yi else None for yi in yinput]
    X = [cinput[i] for i in range(0,len(y)) if y[i] is not None ]
    y = [y[i] for i in range(0,len(y)) if y[i] is not None ]
    print "removed data without required attributes"
    mlb = MultiLabelBinarizer()
    
    X = mlb.fit_transform(X)
    
    print "Created TF-idf vectors"
    
    if y_global==None:
        le = LabelEncoder()
        y = le.fit_transform(y)
        y_global=y
        print "Encoded Labels"
    else:
        y = y_global
    print "Encoded Labels"
    
    # Train Test Split
    return train_test_split(X,y,test_size=0.2,random_state=42)

# MongoDb Connection
client = MongoClient()
db = client.yelp_data
collection = db.review_business_data

# Fetch Data from MongoDB
data = pd.DataFrame(list(collection.find().limit(25000)))
print "Data Loaded from mongodb"


# Preprocessing of data
X=data.text
y = data.attributes
c = data.categories
print "Data to X and y"
print "Majority Classifier"
X_train1,X_test1,y_train,y_test = getBaseLine(X,y,False,1,1)
baselineClassification(X_train1,X_test1,y_train,y_test,"Dummy Majority Classifier","Unigram withot stopwords")
print "*********"
for i in classifiers.keys():

    f= "Bag of words"
    X_train2,X_test2,y_train,y_test = getBaseLine(X,y,False,1,1)
    trainAndTest(X_train2,X_test2,y_train,y_test,i, f)
    print "*********"
    f=  "Bag of words stop words removed"
    X_train3,X_test3,y_train,y_test = getBaseLine(X,y,True,1,1)
    trainAndTest(X_train3,X_test3,y_train,y_test,i, f)
    X_train3=X_train3.toarray()
    X_test3=X_test3.toarray()
    print "*********"
    f=  "Bag of words (bigram) stop words removed"
    Xbigram_train3,Xbigram_test3,y_train,y_test = getBaseLine(X,y,True,2,2)
    trainAndTest(Xbigram_train3,Xbigram_test3,y_train,y_test,i, f)
    print "*********"
    f=  "Bag of words (trigram) stop words removed"
    Xtrigram_train3,Xtrigram_test3,y_train,y_test = getBaseLine(X,y,True,3,3)
    trainAndTest(Xtrigram_train3,Xtrigram_test3,y_train,y_test,i, f)
    print "*********"
    f=  "Bag of words (unigram+bigram) stop words removed"
    Xunibi_train3,Xunibi_test3,y_train,y_test = getBaseLine(X,y,True,1,2)
    trainAndTest(Xunibi_train3,Xunibi_test3,y_train,y_test,i, f)
    print "*********"
    f=  "Bag of words (bigram+triigram) stop words removed"
    Xbitri_train3,Xbitri_test3,y_train,y_test = getBaseLine(X,y,True,2,3)
    trainAndTest(Xbitri_train3,Xbitri_test3,y_train,y_test,i, f)
    print "*********"
    f=  "Bag of words (unigram+bigram+trigram) stop words removed"
    Xall_train3,Xall_test3,y_train,y_test = getBaseLine(X,y,True,1,3)
    trainAndTest(Xall_train3,Xall_test3,y_train,y_test,i, f)
    print "*********"
    f=  "Categories alone"
    X_train4,X_test4,y_train,y_test = getCategories(X,y,c)
    trainAndTest(X_train4,X_test4,y_train,y_test,i, f)
    print "*********"
    f=  "Sentiment Analysis"
    X_train5,X_test5,y_train,y_test = getSentimentPolarity(X,y)
    trainAndTest(X_train5,X_test5,y_train,y_test,i, f)
    print "*********"
    f=  "Bag of words stop words removed & categories"
    Xbowcategories_train=np.append(X_train3,X_train4,axis=1)
    Xbowcategories_test=np.append(X_test3,X_test4,axis=1)
    trainAndTest(Xbowcategories_train,Xbowcategories_test,y_train,y_test,i, f)
    print "*********"
    f=  "Bag of words stop words removed & sentiment analysis"
    Xbowsentiment_train=np.append(X_train3,X_train5,axis=1)
    Xbowsentiment_test=np.append(X_test3,X_test5,axis=1)
    trainAndTest(Xbowsentiment_train,Xbowsentiment_test,y_train,y_test,i, f)
    print "*********"
    f=  "sentiment analysis & categories"
    Xsentimentcategories_train=np.append(X_train4,X_train5,axis=1)
    Xsentimentcategories_test=np.append(X_test4,X_test5,axis=1)
    trainAndTest(Xsentimentcategories_train,Xsentimentcategories_test,y_train,y_test,i, f)
    print "*********"
    f=  "Bag of words stop words removed, categories & sentiment analysis"
    Xbowcategoriessentiment_train=np.append(Xbowcategories_train,X_train5,axis=1)
    Xbowcategoriessentiment_test=np.append(Xbowcategories_test,X_test5,axis=1)
    trainAndTest(Xbowcategoriessentiment_train,Xbowcategoriessentiment_test,y_train,y_test,i, f)

out = csv.writer(open("Delivery.csv", 'wb'), delimiter=',')
out.writerows(csv_output)
