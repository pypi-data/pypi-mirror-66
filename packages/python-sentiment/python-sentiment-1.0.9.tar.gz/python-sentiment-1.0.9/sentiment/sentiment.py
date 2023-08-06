import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import os
t = os.path.abspath(__file__)[:-12]
class Sentiment(ClassifierI):
    
    def __init__(self, *classifiers):
        self._classifiers = classifiers
    
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)
    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

def find_features(document):
    print("Cleaning Input text...")
    document = re.sub(r'[^(a-zA-Z)\s]','', document)
    print("Result after cleaning : ",document)
    words = word_tokenize(document)
    print("Tokenization Results :",words)
    print("Loading stop words from nltk")
    stop_words = list(set(stopwords.words('english')))
    print("Eliminating Stop words from input string...")
    words = [w for w in words if not w in stop_words] 
    print("Resultant list of words : ",words)    
    features = {}
    k = open(t+'all_words.pickle','rb')
    all_words = pickle.load(k)
    k.close()
    all_words = nltk.FreqDist(all_words)
    print("Loading dictionary : (first 5 shown) ",list(all_words)[:5])
    print()
    word_features = list(all_words.keys())
    print("Matching with dictionary and assigning True if present otherwise False")
    for w in word_features:
        features[w] = (w in words)
    return features

def load_model(file_path): 
    classifier_f = open(file_path, "rb")
    classifier = pickle.load(classifier_f)
    classifier_f.close()
    return classifier

def sentiment(text):
    print("Loading prediction model...")
    MNB_Clf = load_model(t+'MNB_clf.pickle')
    ensemble_clf = Sentiment(MNB_Clf)
    print("Processing your text...") 
    feats = find_features(text)
    print("Features extracted and inputted to model: (first 5 shown)",end=' ')
    j=0
    for i in feats:
    	print(i,":",feats[i],";",end=' ')
    	j+=1
    	if (j>5):
    		break
    print()
    return ensemble_clf.classify(feats), ensemble_clf.confidence(feats)
import sys
def main():
    sent = sys.argv[1]
    print("Your sentence was : "+sent)
    dic = {'pos':'positive','neg':'negative'}
    print("Prediction model says that the text is "+dic[sentiment(sent)[0]])

if __name__=="__main__":
    main()