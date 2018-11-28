# -*- coding: utf-8 -*-
import csv
import json
import re
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import stopwords
from sklearn.datasets import load_files

import results_file_handler
import settings
from helper_methods import month_year_iter
from random import randint

def process_news(newspaper, ml_classifier):
    if (newspaper == settings.NEWSPAPERS["el_observador"]["id"]):
        process_el_observador(ml_classifier)

    elif (newspaper == settings.NEWSPAPERS["la_diaria"]["id"]):
        process_la_diaria(ml_classifier)

    elif (newspaper == settings.NEWSPAPERS["busqueda"]["id"]):
        process_busqueda(ml_classifier)


def read_news_count_from_csv(path):
    monthly_news_count = {}
    with open(path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        for row in csvreader:
            monthly_news_count[row[0] + "-" + row[1]] = row[2]
    return monthly_news_count


def process_el_observador(ml_classifier):
    newspaper = settings.NEWSPAPERS["el_observador"]["id"]
    date_from = settings.NEWSPAPERS[newspaper]['datefrom']
    date_to = settings.NEWSPAPERS[newspaper]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    prepare_files(newspaper)

    count_path = settings.NEWS_COUNT_FILEPATH.format(newspaper)
    monthly_news_count = read_news_count_from_csv(count_path)
    
    for date in date_iter:
        year, month = date[0], date[1]
        monthWith0 = ""
        if (month < 10):
            monthWith0 = "0" + str(month)
        else:
            monthWith0 = str(month)
        total_news_month = monthly_news_count[str(year)+"-"+str(month)]
        path = settings.NEWS_JSON_FILEPATH.format(newspaper, str(year), str(monthWith0))
        with open(path, 'r+', encoding='utf-8') as data_file:
            tree = json.load(data_file)
        json_root = tree['add']
        _, epu_news_month = process_json_news(json_root, newspaper, month, year, ml_classifier)
        results_file_handler.save_step1_results(newspaper, month, year, total_news_month, epu_news_month)


def process_la_diaria(ml_classifier):
    newspaper = settings.NEWSPAPERS["la_diaria"]["id"]
    date_from = settings.NEWSPAPERS[newspaper]['datefrom']
    date_to = settings.NEWSPAPERS[newspaper]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    prepare_files(newspaper)

    count_path = settings.NEWS_COUNT_FILEPATH.format(newspaper)
    monthly_news_count = read_news_count_from_csv(count_path)

    for date in date_iter:
        year, month = date[0], date[1]
        total_news_month = monthly_news_count[str(year)+"-"+str(month)]
        path = settings.NEWS_JSON_FILEPATH.format(newspaper, str(year), str(month))
        with open(path, 'r+', encoding='utf-8') as data_file:
            tree = json.load(data_file)
        json_root = tree['add']
        _, epu_news_month = process_json_news(json_root, newspaper, month, year, ml_classifier)
        results_file_handler.save_step1_results(newspaper, month, year, total_news_month, epu_news_month)


def process_busqueda(ml_classifier):
    newspaper = settings.NEWSPAPERS["busqueda"]["id"]
    date_from = settings.NEWSPAPERS[newspaper]['datefrom']
    date_to = settings.NEWSPAPERS[newspaper]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    prepare_files(newspaper)

    for date in date_iter:
        year, month = date[0], date[1]
        path = settings.NEWS_JSON_FILEPATH.format(newspaper, str(year), str(month))
        with open(path, 'r+', encoding='utf-8') as data_file:
            tree = json.load(data_file)
        json_root = tree['add']
        total_news_month, epu_news_month = process_json_news(json_root, newspaper, month, year, ml_classifier)
        results_file_handler.save_step1_results(newspaper, month, year, total_news_month, epu_news_month)


def process_json_news(json_root, newspaper, month, year, ml_classifier):
    total_news_month = 0
    epu_news_month = 0

    for doc in json_root:
        if doc is not None and doc['doc'] is not None and doc['doc']['articulo'] != "":
            total_news_month += 1
            article = doc['doc']['articulo'].lower()
            epu_classification = get_news_epu_classification(article, ml_classifier)
            epu_news_month += epu_classification # Can be 0, 1 or 2

    return total_news_month, epu_news_month


def get_news_epu_classification(article, ml_classifier):
    # vectorizer = CountVectorizer(max_features=1500, min_df=0.5, max_df=5, stop_words=stopwords.words('spanish'))
    # X = vectorizer.fit_transform([article])
    # print(X)
    # epu_classification = ml_classifier.predict(X) # TODO: make this classification work
    # print(epu_classification)
    # return epu_classification
    return randint(0, 2)


def prepare_files(newspaper):
    results_file_handler.delete_results_files(newspaper)
    results_file_handler.create_step1_results_file(newspaper)
