# -*- coding: utf-8 -*-
import json
import xml.etree.ElementTree as ET
import results_handler

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
        '7': 0, # política de seguridad nacional
        '8': 0, # política de regulación financiera
        '9': 0, # política de regulación
        '10': 0, # política de deuda soberana y crisis monetaria
        '11': 0, # política de programas de derechos
        '12': 0, # política comercial
        '13': 0, # otras políticas
        '14': 0 # autoridades
    }
    return dict_category_epu_news

def process_la_republica():
    with open('date_ranges.json') as data_file:
        date_ranges = json.load(data_file)
    date_from = date_ranges['ranges'][0]['datefrom']
    date_to = date_ranges['ranges'][0]['dateto']
    date_iter = month_year_iter(date_from, date_to)

    newspaper = "la_republica"
    results_handler.delete_results_file(newspaper)
    results_handler.create_results_file(newspaper)

    for date in date_iter:
        year, month = date[0], date[1]
        path = "../news/la_republica/" + str(year) + "/" +str(month) + "/la_republica.xml"
        tree = ET.parse(path)
        xml_root = tree.getroot()
        dict_category_epu_news = load_categories_dictionary()
        total_news_month, epu_news_month = process_xml_news(xml_root, dict_category_epu_news)
        results_handler.save_results(newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news)

def process_el_observador():
    #TODO: completar
    print ("No hay noticias para procesar!")

def process_la_diaria():
    #TODO: completar
    print ("No hay noticias para procesar!")

def process_el_pais():
    #TODO: completar
    print ("No hay noticias para procesar!")

def process_xml_news(xml_root, dict_category_epu_news):
    with open('terms.json') as data_file:
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
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][13]["values"]) or
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][14]["values"])):
                    epu_news_month += 1 

                if (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][2]["values"])): 
                    dict_category_epu_news['2'] += 1

                elif (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][3]["values"])): 
                    dict_category_epu_news['3'] += 1

                elif (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][4]["values"])): 
                    dict_category_epu_news['4'] += 1

                elif (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][5]["values"])): 
                    dict_category_epu_news['5'] += 1

                elif (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][6]["values"])): 
                    dict_category_epu_news['6'] += 1

                elif (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][7]["values"])): 
                    dict_category_epu_news['7'] += 1

                elif (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][8]["values"])): 
                    dict_category_epu_news['8'] += 1

                elif (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][9]["values"])): 
                    dict_category_epu_news['9'] += 1

                elif (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][10]["values"])): 
                    dict_category_epu_news['10'] += 1

                elif (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][11]["values"])): 
                    dict_category_epu_news['11'] += 1

                elif (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][12]["values"])): 
                    dict_category_epu_news['12'] += 1

                elif (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][13]["values"])): 
                    dict_category_epu_news['13'] += 1

                elif (any(word.encode('utf-8') in article for word in terms_bag['terms'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in terms_bag['terms'][14]["values"])): 
                    dict_category_epu_news['14'] += 1
    
    return total_news_month, epu_news_month
