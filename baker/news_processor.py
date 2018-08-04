# -*- coding: utf-8 -*-
import csv
import json
import sys
import xml.etree.ElementTree as ET

import results_file_handler
import settings
from helper_methods import *


def read_news_count_from_csv(path):
    monthly_news_count = {}
    with open(path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        for row in csvreader:
            monthly_news_count[row[0] + "-" + row[1]] = row[2]
    return monthly_news_count


def process_la_republica():
    # TODO: ver si se va a usar
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
        total_news_month, epu_news_month = process_xml_news(xml_root, dict_category_epu_news)
        results_file_handler.save_step1_results(
            newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)


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
        _, epu_news_month = process_json_news(json_root, dict_category_epu_news)
        results_file_handler.save_step1_results(
            newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)


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
        _, epu_news_month = process_json_news(json_root, dict_category_epu_news)
        results_file_handler.save_step1_results(
            newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)


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
        total_news_month, epu_news_month = process_xml_news(xml_root, dict_category_epu_news)
        results_file_handler.save_step1_results(
            newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)


def process_busqueda():
    # TODO: implementar
    newspaper = settings.NEWSPAPERS["busqueda"]["id"]
    print("\nNo se tienen noticias de Búsqueda para procesar.\n")
    sys.exit()


def check_if_news_is_epu(article, dict_category_epu_news, category_index):
    if (any(word.encode('utf-8') in article for word in settings.TERMS_BAG[0]["values"]) and
            any(word.encode('utf-8') in article for word in settings.TERMS_BAG[1]["values"])) and (
            any(word.encode('utf-8') in article for word in settings.TERMS_BAG[category_index]["values"])):
        dict_category_epu_news[str(category_index)] += 1
        return True
    return False


def process_xml_news(xml_root, dict_category_epu_news):
    total_news_month = 0
    epu_news_month = 0

    for doc in xml_root:
        for field in doc:
            found_epu_news = False
            if field.get('name') == 'articulo':
                total_news_month += 1  # TODO: chequear por qué da 8000 noticias a la republica
                article = field.text.lower().encode('utf-8')
                for i in range(2, settings.CATEGORIES_COUNT + 2):
                    is_epu = check_if_news_is_epu(article, dict_category_epu_news, i)
                    if is_epu and not found_epu_news:
                        found_epu_news = True
                        epu_news_month += 1

    return total_news_month, epu_news_month


def process_json_news(json_root, dict_category_epu_news):
    total_news_month = 0
    epu_news_month = 0

    for doc in json_root:
        if doc is not None and doc['doc'] is not None and doc['doc']['articulo'] != "":
            total_news_month += 1
            found_epu_news = False
            article = doc['doc']['articulo'].lower().encode('utf-8')
            for i in range(2, settings.CATEGORIES_COUNT + 2):
                is_epu = check_if_news_is_epu(article, dict_category_epu_news, i)
                if is_epu and not found_epu_news:
                    found_epu_news = True
                    epu_news_month += 1

    return total_news_month, epu_news_month
