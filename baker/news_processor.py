# -*- coding: utf-8 -*-
import csv
import json
import re
import sys
import xml.etree.ElementTree as ET

import results_file_handler
import settings
from helper_methods import *


def process_news(newspaper):
    if (newspaper == settings.NEWSPAPERS["el_observador"]["id"]):
        process_el_observador()

    elif (newspaper == settings.NEWSPAPERS["la_diaria"]["id"]):
        process_la_diaria()

    elif (newspaper == settings.NEWSPAPERS["busqueda"]["id"]):
        process_busqueda()


def read_news_count_from_csv(path):
    monthly_news_count = {}
    with open(path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        for row in csvreader:
            monthly_news_count[row[0] + "-" + row[1]] = row[2]
    return monthly_news_count


def process_la_republica():
    # No se va a usar porque se tienen pocos años
    newspaper = settings.NEWSPAPERS["la_republica"]["id"]
    date_from = settings.NEWSPAPERS[newspaper]['datefrom']
    date_to = settings.NEWSPAPERS[newspaper]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    results_file_handler.delete_results_files(newspaper)
    results_file_handler.create_step1_results_file(newspaper)

    for date in date_iter:
        year, month = date[0], date[1]
        path = settings.NEWS_XML_FILEPATH.format(newspaper, str(year), str(month))
        tree = ET.parse(path)
        xml_root = tree.getroot()
        dict_category_epu_news = load_categories_dictionary()
        total_news_month, economy_news_month, epu_news_month, eu_news_month = process_xml_news(xml_root, dict_category_epu_news)
        results_file_handler.save_step1_results(
            newspaper, month, year, total_news_month, economy_news_month, epu_news_month, eu_news_month, dict_category_epu_news)


def process_el_observador():
    newspaper = settings.NEWSPAPERS["el_observador"]["id"]
    date_from = settings.NEWSPAPERS[newspaper]['datefrom']
    date_to = settings.NEWSPAPERS[newspaper]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    results_file_handler.delete_results_files(newspaper)
    results_file_handler.create_step1_results_file(newspaper)

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
        dict_category_epu_news = load_categories_dictionary()
        _, economy_news_month, epu_news_month, eu_news_month = process_json_news(json_root, dict_category_epu_news)
        results_file_handler.save_step1_results(
            newspaper, month, year, total_news_month, economy_news_month, epu_news_month, eu_news_month, dict_category_epu_news)


def process_la_diaria():
    newspaper = settings.NEWSPAPERS["la_diaria"]["id"]
    date_from = settings.NEWSPAPERS[newspaper]['datefrom']
    date_to = settings.NEWSPAPERS[newspaper]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    results_file_handler.delete_results_files(newspaper)
    results_file_handler.create_step1_results_file(newspaper)

    count_path = settings.NEWS_COUNT_FILEPATH.format(newspaper)
    monthly_news_count = read_news_count_from_csv(count_path)

    for date in date_iter:
        year, month = date[0], date[1]
        total_news_month = monthly_news_count[str(year)+"-"+str(month)]
        path = settings.NEWS_JSON_FILEPATH.format(newspaper, str(year), str(month))
        with open(path, 'r+', encoding='utf-8') as data_file:
            tree = json.load(data_file)
        json_root = tree['add']
        dict_category_epu_news = load_categories_dictionary()
        _, economy_news_month, epu_news_month, eu_news_month = process_json_news(json_root, dict_category_epu_news)
        results_file_handler.save_step1_results(
            newspaper, month, year, total_news_month, economy_news_month, epu_news_month, eu_news_month, dict_category_epu_news)


def process_el_pais():
    # No se va a usar porque los datos no eran muy confiables
    newspaper = settings.NEWSPAPERS["el_pais"]["id"]
    date_from = settings.NEWSPAPERS[newspaper]['datefrom']
    date_to = settings.NEWSPAPERS[newspaper]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    results_file_handler.delete_results_files(newspaper)
    results_file_handler.create_step1_results_file(newspaper)

    for date in date_iter:
        year, month = date[0], date[1]
        path = settings.NEWS_XML_FILEPATH.format(newspaper, str(year), str(month))
        tree = ET.parse(path)
        xml_root = tree.getroot()
        dict_category_epu_news = load_categories_dictionary()
        total_news_month, economy_news_month, epu_news_month, eu_news_month = process_xml_news(xml_root, dict_category_epu_news)
        results_file_handler.save_step1_results(
            newspaper, month, year, total_news_month, economy_news_month, epu_news_month, eu_news_month, dict_category_epu_news)


def process_busqueda():
    newspaper = settings.NEWSPAPERS["busqueda"]["id"]
    date_from = settings.NEWSPAPERS[newspaper]['datefrom']
    date_to = settings.NEWSPAPERS[newspaper]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    results_file_handler.delete_results_files(newspaper)
    results_file_handler.create_step1_results_file(newspaper)

    for date in date_iter:
        year, month = date[0], date[1]
        path = settings.NEWS_JSON_FILEPATH.format(newspaper, str(year), str(month))
        with open(path, 'r+', encoding='utf-8') as data_file:
            tree = json.load(data_file)
        json_root = tree['add']
        dict_category_epu_news = load_categories_dictionary()
        total_news_month, economy_news_month, epu_news_month, eu_news_month = process_json_news(json_root, dict_category_epu_news)
        results_file_handler.save_step1_results(
            newspaper, month, year, total_news_month, economy_news_month, epu_news_month, eu_news_month, dict_category_epu_news)


def check_if_news_is_epu(article, dict_category_epu_news, category_index):
    is_economy = False
    is_epu = False
    is_eu = False

    if (any(find_whole_word(word)(article) for word in settings.TERMS_BAG[0]["values"])):
        is_economy = True
        
        if (any(find_whole_word(word)(article) for word in settings.TERMS_BAG[1]["values"])):
            is_eu = True

            if (any(find_whole_word(word)(article) for word in settings.TERMS_BAG[category_index]["values"])):
                is_epu = True
                dict_category_epu_news[str(category_index)] += 1
    
    return is_economy, is_epu, is_eu


def find_whole_word(word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search


def process_xml_news(xml_root, dict_category_epu_news):
    total_news_month = 0
    economy_news_month = 0
    epu_news_month = 0
    eu_news_month = 0

    for doc in xml_root:
        for field in doc:
            found_economy_news = False
            found_epu_news = False
            found_eu_news = False
            if field.get('name') == 'articulo':
                total_news_month += 1
                article = field.text.lower().encode('utf-8') # TODO: check if .encode is necessary (in json its not)
                for i in range(2, settings.COLUMNS_COUNT_2):
                    is_economy, is_epu, is_eu = check_if_news_is_epu(article, dict_category_epu_news, i)
                    if is_economy and not found_economy_news:
                        found_economy_news = True
                        economy_news_month += 1
                    if is_epu and not found_epu_news:
                        found_epu_news = True
                        epu_news_month += 1
                    if is_eu and not found_eu_news:
                        found_eu_news = True
                        eu_news_month += 1

    return total_news_month, economy_news_month, epu_news_month, eu_news_month


def process_json_news(json_root, dict_category_epu_news):
    total_news_month = 0
    economy_news_month = 0
    epu_news_month = 0
    eu_news_month = 0

    for doc in json_root:
        if doc is not None and doc['doc'] is not None and doc['doc']['articulo'] != "":
            total_news_month += 1
            found_economy_news = False
            found_epu_news = False
            found_eu_news = False
            article = doc['doc']['articulo'].lower()
            for i in range(2, settings.COLUMNS_COUNT_2):
                is_economy, is_epu, is_eu = check_if_news_is_epu(article, dict_category_epu_news, i)
                if is_economy and not found_economy_news:
                    found_economy_news = True
                    economy_news_month += 1
                if is_epu and not found_epu_news:
                    found_epu_news = True
                    epu_news_month += 1
                if is_eu and not found_eu_news:
                    found_eu_news = True
                    eu_news_month += 1

    return total_news_month, economy_news_month, epu_news_month, eu_news_month
