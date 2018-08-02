# -*- coding: utf-8 -*-
import json
import csv
import xml.etree.ElementTree as ET
import results_file_handler
import sys
from helper_methods import *

def read_news_count_from_csv(path):
    monthly_news_count = {}
    with open(path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')        
        next(csvreader)        
        for row in csvreader:
            monthly_news_count[row[0]+ "-" + row[1]] = row[2]                       
    return monthly_news_count

def process_la_republica():
    with open('date_ranges.json', 'r+', encoding='utf-8') as data_file:
        date_ranges = json.load(data_file)
    date_from = date_ranges['ranges'][0]['datefrom']
    date_to = date_ranges['ranges'][0]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    newspaper = "la_republica"
    results_file_handler.delete_results_files(newspaper)
    results_file_handler.create_step1_results_file(newspaper)

    for date in date_iter:
        year, month = date[0], date[1]
        path = "../news/la_republica/" + str(year) + "/" +str(month) + "/la_republica.xml"
        tree = ET.parse(path)
        xml_root = tree.getroot()
        dict_category_epu_news = load_categories_dictionary()
        total_news_month, epu_news_month = process_xml_news(xml_root, dict_category_epu_news)
        results_file_handler.save_step1_results(newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)

def process_el_observador():
    with open('date_ranges.json', 'r+', encoding='utf-8') as data_file:
        date_ranges = json.load(data_file)
    date_from = date_ranges['ranges'][1]['datefrom']
    date_to = date_ranges['ranges'][1]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    newspaper = "el_observador"
    results_file_handler.delete_results_files(newspaper)
    results_file_handler.create_step1_results_file(newspaper)  

    path = '../news/el_observador/cant_noticias_el_observador.csv'
    monthly_news_count = read_news_count_from_csv(path)    

    for date in date_iter:
        year, month = date[0], date[1]
        monthWith0 = ""
        if (month < 10):
            monthWith0 = "0"+ str(month)
        else:
            monthWith0 = str(month)        
        total_news_month = monthly_news_count[str(year)+"-"+str(month)]        
        path = "../news/el_observador/" + str(year) + "/" + monthWith0 + "/data.json"                      
        with open(path, 'r+', encoding='utf-8') as data_file:
            tree = json.load(data_file)                        
        json_root = tree['add']        
        dict_category_epu_news = load_categories_dictionary()
        _, epu_news_month = process_json_news(json_root, dict_category_epu_news)
        results_file_handler.save_step1_results(newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)

def process_la_diaria():
    with open('date_ranges.json', 'r+', encoding='utf-8') as data_file:
        date_ranges = json.load(data_file)
    date_from = date_ranges['ranges'][2]['datefrom']
    date_to = date_ranges['ranges'][2]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    newspaper = "la_diaria"
    results_file_handler.delete_results_files(newspaper)
    results_file_handler.create_step1_results_file(newspaper)  

    path = '../news/la_diaria/cant_noticias_la_diaria.csv'
    monthly_news_count = read_news_count_from_csv(path)    

    for date in date_iter:
        year, month = date[0], date[1]     
        total_news_month = monthly_news_count[str(year)+"-"+str(month)]        
        path = "../news/la_diaria/" + str(year) + "/" + str(month) + "/data.json"                      
        with open(path, 'r+', encoding='utf-8') as data_file:
            tree = json.load(data_file)                        
        json_root = tree['add']        
        dict_category_epu_news = load_categories_dictionary()
        _, epu_news_month = process_json_news(json_root, dict_category_epu_news)
        results_file_handler.save_step1_results(newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)

def process_el_pais():
    # No se va a usar porque los datos no eran muy confiables
    with open('date_ranges.json', 'r+', encoding='utf-8') as data_file:
        date_ranges = json.load(data_file)
    date_from = date_ranges['ranges'][2]['datefrom']
    date_to = date_ranges['ranges'][2]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    newspaper = "el_pais"
    results_file_handler.delete_results_files(newspaper)
    results_file_handler.create_step1_results_file(newspaper)

    for date in date_iter:
        year, month = date[0], date[1]
        path = "../news/el_pais/" + str(year) + "/" +str(month) + "/el_pais.xml"
        tree = ET.parse(path)
        xml_root = tree.getroot()
        dict_category_epu_news = load_categories_dictionary()
        total_news_month, epu_news_month = process_xml_news(xml_root, dict_category_epu_news)
        results_file_handler.save_step1_results(newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)

def process_busqueda():
    # TODO: implementar
    print("\nNo se tienen noticias de Búsqueda para procesar.\n")
    sys.exit()

def check_if_news_is_epu(article, terms_bag, dict_category_epu_news, category_index):
    if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
        any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
        any(word.encode('utf-8') in article for word in terms_bag['terms'][category_index]["values"])): 
        dict_category_epu_news[str(category_index)] += 1
        return True
    return False

def process_xml_news(xml_root, dict_category_epu_news):
    with open('terms.json', 'r+', encoding='utf-8') as data_file:
        terms_bag = json.load(data_file)
    
    total_news_month = 0
    epu_news_month = 0
    cat_count = categories_count()

    for doc in xml_root:
        for field in doc:
            found_epu_news = False
            if field.get('name') == 'articulo':
                total_news_month += 1 # TODO: chequear por qué da 8000 noticias a la republica
                article = field.text.lower().encode('utf-8')        
                for i in range(2, cat_count + 2):
                    is_epu = check_if_news_is_epu(article, terms_bag, dict_category_epu_news, i)
                    if is_epu and not found_epu_news:
                        found_epu_news = True
                        epu_news_month += 1

    return total_news_month, epu_news_month

def process_json_news(json_root, dict_category_epu_news):
    with open('terms.json', 'r+', encoding='utf-8') as data_file:
        terms_bag = json.load(data_file)
    
    total_news_month = 0
    epu_news_month = 0
    cat_count = categories_count()

    for doc in json_root:
        if doc is not None and doc['doc'] is not None and doc['doc']['articulo'] != "":
            total_news_month += 1
            found_epu_news = False
            article = doc['doc']['articulo'].lower().encode('utf-8')
            for i in range(2, cat_count + 2):
                is_epu = check_if_news_is_epu(article, terms_bag, dict_category_epu_news, i)
                if is_epu and not found_epu_news:
                    found_epu_news = True
                    epu_news_month += 1

    return total_news_month, epu_news_month
