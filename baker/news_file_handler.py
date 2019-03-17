# -*- coding: utf-8 -*-
import csv
import json
import os
import re
import os.path
from datetime import date

import settings


def delete_processed_news_files(newspaper):
    delete_economy_news_files(newspaper)
    delete_eu_news_files(newspaper)
    delete_non_economy_news_files(newspaper)


def delete_economy_news_files(newspaper):
    path = settings.NEWS_ECONOMY_DIRECTORY.format(newspaper)
    for root, _, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))


def delete_eu_news_files(newspaper):
    path = settings.NEWS_EU_DIRECTORY.format(newspaper)
    for root, _, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))


def delete_non_economy_news_files(newspaper):
    path = settings.NEWS_NON_ECONOMY_DIRECTORY.format(newspaper)
    for root, _, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))


def write_economy_news_to_file(doc, newspaper, month, year):
    file_path = settings.NEWS_ECONOMY_JSON_FILEPATH.format(newspaper, str(year), str(month))
    write_news_to_file(doc, file_path)


def write_eu_news_to_file(doc, newspaper, month, year):
    file_path = settings.NEWS_EU_JSON_FILEPATH.format(newspaper, str(year), str(month))
    write_news_to_file(doc, file_path)


def write_non_economy_news_to_file(doc, newspaper, month, year):
    file_path = settings.NEWS_NON_ECONOMY_JSON_FILEPATH.format(newspaper, str(year), str(month))
    write_news_to_file(doc, file_path)


def write_news_to_file(doc, file_path):
    if settings.WRITE_PROCESSED_NEWS:
        if os.path.isfile(file_path): # File already exists
            append_to_file(doc, file_path)
        else:
            create_and_write_file(doc, file_path)


def create_and_write_file(doc, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    docs_array = {}
    docs_array["add"] = []
    docs_array["add"].append(doc)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(docs_array, f, ensure_ascii=False)


def append_to_file(doc, file_path):
    with open(file_path, encoding='utf-8') as feedsjson:
        docs_array = json.load(feedsjson)
    docs_array["add"].append(doc)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(docs_array, f, ensure_ascii=False)
