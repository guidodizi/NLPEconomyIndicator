# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

def process_news_el_pais(year, month, terms_bag, dict_category_epu_news):
    # aca vendría abrir dinamico dependiendo de la fecha
    #path = 'news/el_pais/' + year + '/' + month + '/'
    tree = ET.parse('../news/el_pais/elpais20140926203240Noticias.xml')
    add = tree.getroot()

    total_news_month, epu_news_month = process_xml_news(add, terms_bag, dict_category_epu_news)
    return total_news_month, epu_news_month

def process_news_la_republica(year, month, terms_bag, dict_category_epu_news):
    # aca vendría abrir dinamico dependiendo de la fecha
    #path = 'news/la_republica/' + year + '/' + month + '/'
    tree = ET.parse('../news/la_republica/2011_2014_la_republica.xml')
    add = tree.getroot()

    total_news_month, epu_news_month = process_xml_news(add, terms_bag, dict_category_epu_news)
    return total_news_month, epu_news_month

def process_news_el_observador(year, month, terms_bag, dict_category_epu_news):
    #TODO: completar
    return 0, 0

def process_news_la_diaria(year, month, terms_bag, dict_category_epu_news):
    #TODO: completar
    return 0, 0

def process_xml_news(add, terms_bag, dict_category_epu_news):
    total_news_month = 0
    epu_news_month = 0

    for doc in add:
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

            total_news_month += 1

    return total_news_month, epu_news_month
