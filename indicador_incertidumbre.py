# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

def monthly_indicator_by_category(newspaper, year, month,  bag_of_words):
    """
    Función que calcula el índice para un diario y fecha dados. 
    
    Params: 
        diario: indica qué diario a procesar. 
        fecha: indica el mes y año en formato mm-aaaa. 

    Returns: 
        Devuelve una tupla (A,B)
        A: total de noticias del mes. 
        B: cantidad noticias EPU del mes. 
        C: diccionario con la cantidad de noticias EPU por categoría. 
    """
    news_qty_month = 0
    # total_noticias_mes = cantidad_articulos(newspaper)
    news_epu_month = 0
    
    qty_by_category = {
        '2': 0,  # política impositiva
        '3': 0,  # política de gasto gubernamental
        '4': 0,  # política fiscal
        '5': 0,  # política monetaria
        '6': 0,  # política de salud
        '7': 0,  # política de seguridad nacional
        '8': 0,  # política de regulación financiera
        '9': 0,  # política de regulación
        '10': 0,  # política de deuda soberana y crisis monetaria
        '11': 0,  # política de programas de derechos
        '12': 0,  # política comercial
        '13': 0,  # otras políticas
        '14': 0  # autoridades
    }

    # PROCESAR NOTICIAS Y DEVOLVER RESULTADOS
    if (newspaper == "el_pais"):
        news_qty_month, news_epu_month = process_news_el_pais(year, month, bag_of_words, qty_by_category)
    elif (newspaper == "el_observador"):
        news_qty_month, news_epu_month = process_news_el_observador(year, month, bag_of_words, qty_by_category)
    elif (newspaper == "la_diaria"):
        news_qty_month, news_epu_month = process_news_la_diaria(year, month, bag_of_words, qty_by_category)
    elif (newspaper == "la_republica"):
        news_qty_month, news_epu_month = process_news_la_republica(year, month, bag_of_words, qty_by_category)

    return news_qty_month, news_epu_month, qty_by_category

def process_news_el_pais(year, month, bag_of_words, qty_by_category):
    # aca vendría abrir dinamico dependiendo de la fecha
    #path = 'news/el_pais/' + year + '/' + month + '/'  
    tree = ET.parse('news/el_pais/elpais20140926203240Noticias.xml')
    add = tree.getroot()

    news_qty_month, news_epu_month = parse_xml(add,bag_of_words, qty_by_category)
    return news_qty_month, news_epu_month

def process_news_el_observador(year, month, bag_of_words, qty_by_category):
    # aca vendría abrir dinamico dependiendo de la fecha
    #path = 'news/la_republica/' + year + '/' + month + '/' 
    tree = ET.parse('news/el_observador/larepublica20141107112348Noticias.xml')
    add = tree.getroot()

    news_qty_month, news_epu_month = parse_xml(add,bag_of_words, qty_by_category)
    return news_qty_month, news_epu_month

def process_news_la_diaria(year, month, bag_of_words, qty_by_category):
    # aca vendría abrir dinamico dependiendo de la fecha
    #path = 'news/la_diaria/' + year + '/' + month + '/'  
    tree = ET.parse('news/la_republica/larepublica20141107112348Noticias.xml')
    add = tree.getroot()

    news_qty_month, news_epu_month = parse_xml(add,bag_of_words, qty_by_category)
    return news_qty_month, news_epu_month

def process_news_la_republica(year, month, bag_of_words, qty_by_category):

    # aca vendría abrir dinamico dependiendo de la fecha
    #path = 'news/la_republica/' + year + '/' + month + '/' 
    tree = ET.parse('news/la_republica/larepublica20141107112348Noticias.xml')
    add = tree.getroot()

    news_qty_month, news_epu_month = parse_xml(add,bag_of_words, qty_by_category)
    return news_qty_month, news_epu_month

def parse_xml(add, bag_of_words, qty_by_category):
    
    news_qty_month = 0 
    news_epu_month = 0 

    for doc in add:
        for field in doc:   
            if field.get('name') == 'articulo':
                article = field.text.lower().encode('utf-8')
                if ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][2]["values"]) or 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][3]["values"]) or
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][4]["values"]) or
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][5]["values"]) or
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][6]["values"]) or
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][7]["values"]) or
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][8]["values"]) or
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][9]["values"]) or
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][10]["values"]) or
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][11]["values"]) or
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][12]["values"]) or
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][13]["values"]) or
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][14]["values"])):
                    news_epu_month += 1 

                if ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][2]["values"])): 
                    qty_by_category['2'] += 1
                elif ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][3]["values"])): 
                    qty_by_category['3'] += 1
                elif ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][4]["values"])): 
                    qty_by_category['4'] += 1
                elif ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][5]["values"])): 
                    qty_by_category['5'] += 1
                elif ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][6]["values"])): 
                    qty_by_category['6'] += 1
                elif ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][7]["values"])): 
                    qty_by_category['7'] += 1
                elif ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][8]["values"])): 
                    qty_by_category['8'] += 1
                elif ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][9]["values"])): 
                    qty_by_category['9'] += 1
                elif ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][10]["values"])): 
                    qty_by_category['10'] += 1
                elif ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][11]["values"])): 
                    qty_by_category['11'] += 1
                elif ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][12]["values"])): 
                    qty_by_category['12'] += 1
                elif ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][13]["values"])): 
                    qty_by_category['13'] += 1
                elif ( any(word.encode('utf-8') in article for word in bag_of_words['concepts'][0]["values"]) and 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][1]["values"]) ) and ( 
                    any(word.encode('utf-8') in article for word in bag_of_words['concepts'][14]["values"])): 
                    qty_by_category['14'] += 1
            news_qty_month += 1
    return news_qty_month, news_epu_month