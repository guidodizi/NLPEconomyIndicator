import json
import settings
import re
import nltk
import pickle
import numpy as np
import glob
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import stopwords
from sklearn.datasets import load_files
# nltk.download('stopwords')


def generate_training_set_dataturks():
    path = "training_sets/small_training_news_60.json"
    cat0_path = "data/0/"
    cat1_path = "data/1/"
    cat2_path = "data/2/"
    f = open(path, "r", encoding="utf-8")
    if f.mode == "r":
        lines = f.readlines()
        i = 0
        for l in lines:
            obj = json.loads(l)
            labels = obj['annotation']['labels']
            category = -1
            if labels:
                category = re.findall(r'\d+',labels[0])[0]
            if (category == '0'):
                f= open(cat0_path + str(i) + '.txt',"w+")
                f.write(obj['content'])
                f.close()
            elif (category == '1'):
                f= open(cat1_path + str(i) + '.txt',"w+")
                f.write(obj['content'])
                f.close()
            elif (category == '2'):
                f= open(cat2_path + str(i) + '.txt',"w+")
                f.write(obj['content'])
                f.close()
            i += 1


def generate_training_set_tagtog():
    txt_list = [x for x in os.listdir(settings.TAGTOG_PATH) if x.endswith(".txt")]
    json_list = [x for x in os.listdir(settings.TAGTOG_PATH) if x.endswith(".json")]
    i = 0
    for txt in txt_list:
        f = open(settings.TAGTOG_PATH + txt, "r", encoding="utf-8")
        text = f.read()
        txt_name = txt.rsplit(".",1)[0]
        json_name = txt_name + ".ann.json"
        if json_name in json_list:
            with open(settings.TAGTOG_PATH + json_name, 'r+', encoding='utf-8') as data_file:
                data = json.load(data_file)
            key = settings.TAGTOG_KEY_NAME
            if key in data["metas"]:
                category = data["metas"][key]["value"]
                if (category == '0'):
                    f= open(settings.CAT0_PATH + str(i) + '.txt',"w+")
                    f.write(text)
                    f.close()
                elif (category == '1'):
                    f= open(settings.CAT1_PATH + str(i) + '.txt',"w+")
                    f.write(text)
                    f.close()
                elif (category == '2'):
                    f= open(settings.CAT2_PATH + str(i) + '.txt',"w+")
                    f.write(text)
                    f.close()
                i += 1


def text_preproccessing():
    data = load_files(r"data")
    X, y = data.data, data.target
    documents = []
    for sen in range(0, len(X)):
        # Remove all the special characters
        document = re.sub(r'\W', ' ', str(X[sen]))

        # remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

        # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)

        # Removing prefixed 'b'
        document = re.sub(r'^b\s+', '', document)

        # Converting to Lowercase
        document = document.lower()

        # Lemmatization
        #document = document.split()

        #document = [stemmer.lemmatize(word) for word in document]
        #document = ' '.join(document)

        documents.append(document)

    vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('spanish'))
    X = vectorizer.fit_transform(documents).toarray()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print(accuracy_score(y_test, y_pred))

    return classifier
