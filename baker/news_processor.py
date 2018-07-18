# -*- coding: utf-8 -*-
import json
import csv
import xml.etree.ElementTree as ET
import results_handler
import sys

def month_year_iter(date_from, date_to):
    start_month = int(date_from.split("-")[0])
    start_year = int(date_from.split("-")[1])
    end_month = int(date_to.split("-")[0])
    end_year = int(date_to.split("-")[1])
    ym_start= 12 * start_year + start_month - 1
    ym_end= 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m+1

def load_categories_dictionary():
    dict_category_epu_news = {
        '2': 0, # política impositiva
        '3': 0, # política de gasto gubernamental
        '4': 0, # política fiscal
        '5': 0, # política monetaria
        '6': 0, # política de salud
        '7': 0, # política de regulación financiera
        '8': 0, # política de regulación
        '9': 0, # política de deuda soberana y crisis monetaria
        '10': 0, # política de programas de derechos
        '11': 0, # política comercial
        '12': 0, # otras políticas
        '13': 0 # autoridades internacionales
    }
    return dict_category_epu_news

def load_total_news_all_months(path):
    total_news_all_month = {}
    with open(path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')        
        next(csvreader)        
        for row in csvreader:
            total_news_all_month[row[0]+ "-" + row[1]] = row[2]                       
    return total_news_all_month

def process_la_republica():
    with open('date_ranges.json', 'r+', encoding='utf-8') as data_file:
        date_ranges = json.load(data_file)
    date_from = date_ranges['ranges'][0]['datefrom']
    date_to = date_ranges['ranges'][0]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    newspaper = "la_republica"
    results_handler.delete_results_files(newspaper)
    results_handler.create_step1_results_file(newspaper)

    for date in date_iter:
        year, month = date[0], date[1]
        path = "../news/la_republica/" + str(year) + "/" +str(month) + "/la_republica.xml"
        tree = ET.parse(path)
        xml_root = tree.getroot()
        dict_category_epu_news = load_categories_dictionary()
        total_news_month, epu_news_month = process_xml_news(xml_root, dict_category_epu_news)
        results_handler.save_step1_results(newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)

def process_el_observador():
    with open('date_ranges.json', 'r+', encoding='utf-8') as data_file:
        date_ranges = json.load(data_file)
    date_from = date_ranges['ranges'][1]['datefrom']
    date_to = date_ranges['ranges'][1]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    newspaper = "el_observador"
    results_handler.delete_results_files(newspaper)
    results_handler.create_step1_results_file(newspaper)  

    path = '../news/el_observador/cant_noticias_el_observador.csv'
    total_news_all_month = load_total_news_all_months(path)    

    for date in date_iter:
        year, month = date[0], date[1]
        monthWith0 = ""
        if (month < 10):
            monthWith0 = "0"+ str(month)
        else:
            monthWith0 = str(month)        
        total_news_month = total_news_all_month[str(year)+"-"+str(month)]        
        path = "../news/el_observador/" + str(year) + "/" + monthWith0 + "/data.json"                      
        with open(path, 'r+', encoding='utf-8') as data_file:
            tree = json.load(data_file)                        
        json_root = tree['add']        
        dict_category_epu_news = load_categories_dictionary()
        epu_news_month = process_json_news(json_root, dict_category_epu_news)
        results_handler.save_step1_results(newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)

def process_la_diaria():
    with open('date_ranges.json', 'r+', encoding='utf-8') as data_file:
        date_ranges = json.load(data_file)
    date_from = date_ranges['ranges'][2]['datefrom']
    date_to = date_ranges['ranges'][2]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    newspaper = "la_diaria"
    results_handler.delete_results_files(newspaper)
    results_handler.create_step1_results_file(newspaper)  

    path = '../news/la_diaria/cant_noticias_la_diaria.csv'
    total_news_all_month = load_total_news_all_months(path)    

    for date in date_iter:
        year, month = date[0], date[1]     
        total_news_month = total_news_all_month[str(year)+"-"+str(month)]        
        path = "../news/la_diaria/" + str(year) + "/" + str(month) + "/data.json"                      
        with open(path, 'r+', encoding='utf-8') as data_file:
            tree = json.load(data_file)                        
        json_root = tree['add']        
        dict_category_epu_news = load_categories_dictionary()
        epu_news_month = process_json_news(json_root, dict_category_epu_news)
        results_handler.save_step1_results(newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)

def process_el_pais():
    # No se va a usar porque los datos no eran muy confiables
    with open('date_ranges.json', 'r+', encoding='utf-8') as data_file:
        date_ranges = json.load(data_file)
    date_from = date_ranges['ranges'][2]['datefrom']
    date_to = date_ranges['ranges'][2]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    newspaper = "el_pais"
    results_handler.delete_results_files(newspaper)
    results_handler.create_step1_results_file(newspaper)

    for date in date_iter:
        year, month = date[0], date[1]
        path = "../news/el_pais/" + str(year) + "/" +str(month) + "/el_pais.xml"
        tree = ET.parse(path)
        xml_root = tree.getroot()
        dict_category_epu_news = load_categories_dictionary()
        total_news_month, epu_news_month = process_xml_news(xml_root, dict_category_epu_news)
        results_handler.save_step1_results(newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)
    sys.exit()

def process_xml_news(xml_root, dict_category_epu_news):
    with open('terms.json', 'r+', encoding='utf-8') as data_file:
        terms_bag = json.load(data_file)
    
    total_news_month = 0
    epu_news_month = 0

    for doc in xml_root:
        total_news_month += 1
        for field in doc:
            if field.get('name') == 'articulo':
                article = field.text.lower().encode('utf-8')
                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][2]["values"]) or 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][3]["values"]) or
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][4]["values"]) or
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][5]["values"]) or
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][6]["values"]) or
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][7]["values"]) or
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][8]["values"]) or
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][9]["values"]) or
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][10]["values"]) or
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][11]["values"]) or
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][12]["values"]) or
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][13]["values"])):
                    epu_news_month += 1 

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][2]["values"])): 
                    dict_category_epu_news['2'] += 1

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][3]["values"])): 
                    dict_category_epu_news['3'] += 1

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][4]["values"])): 
                    dict_category_epu_news['4'] += 1

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][5]["values"])): 
                    dict_category_epu_news['5'] += 1

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][6]["values"])): 
                    dict_category_epu_news['6'] += 1

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][7]["values"])): 
                    dict_category_epu_news['7'] += 1

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][8]["values"])): 
                    dict_category_epu_news['8'] += 1

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][9]["values"])): 
                    dict_category_epu_news['9'] += 1

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][10]["values"])): 
                    dict_category_epu_news['10'] += 1

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][11]["values"])): 
                    dict_category_epu_news['11'] += 1

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][12]["values"])): 
                    dict_category_epu_news['12'] += 1

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][13]["values"])): 
                    dict_category_epu_news['13'] += 1
    
    return total_news_month, epu_news_month

def process_json_news(json_root, dict_category_epu_news):
    with open('terms.json', 'r+', encoding='utf-8') as data_file:
        terms_bag = json.load(data_file)
    
    epu_news_month = 0      
    for doc in json_root:                           
        if doc is not None and doc['doc'] is not None and doc['doc']['articulo'] != "":            
            article = doc['doc']['articulo'].lower().encode('utf-8')
            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][2]["values"]) or 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][3]["values"]) or
                any(word.encode('utf-8') in article for word in terms_bag['terms'][4]["values"]) or
                any(word.encode('utf-8') in article for word in terms_bag['terms'][5]["values"]) or
                any(word.encode('utf-8') in article for word in terms_bag['terms'][6]["values"]) or
                any(word.encode('utf-8') in article for word in terms_bag['terms'][7]["values"]) or
                any(word.encode('utf-8') in article for word in terms_bag['terms'][8]["values"]) or
                any(word.encode('utf-8') in article for word in terms_bag['terms'][9]["values"]) or
                any(word.encode('utf-8') in article for word in terms_bag['terms'][10]["values"]) or
                any(word.encode('utf-8') in article for word in terms_bag['terms'][11]["values"]) or
                any(word.encode('utf-8') in article for word in terms_bag['terms'][12]["values"]) or
                any(word.encode('utf-8') in article for word in terms_bag['terms'][13]["values"])):
                epu_news_month += 1 

            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][2]["values"])): 
                dict_category_epu_news['2'] += 1

            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][3]["values"])): 
                dict_category_epu_news['3'] += 1

            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][4]["values"])): 
                dict_category_epu_news['4'] += 1

            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][5]["values"])): 
                dict_category_epu_news['5'] += 1

            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][6]["values"])): 
                dict_category_epu_news['6'] += 1

            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][7]["values"])): 
                dict_category_epu_news['7'] += 1

            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][8]["values"])): 
                dict_category_epu_news['8'] += 1

            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][9]["values"])): 
                dict_category_epu_news['9'] += 1

            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][10]["values"])): 
                dict_category_epu_news['10'] += 1

            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][11]["values"])): 
                dict_category_epu_news['11'] += 1

            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][12]["values"])): 
                dict_category_epu_news['12'] += 1

            if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in terms_bag['terms'][13]["values"])): 
                dict_category_epu_news['13'] += 1
    
    return epu_news_month
