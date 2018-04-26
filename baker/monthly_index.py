# -*- coding: utf-8 -*-
from process_news import *

def monthly_indicator_by_category(newspaper, year, month,  terms_bag):
    """
    Función que calcula el índice para un diario y fecha dados. 
    
    Params: 
        diario: indica qué diario a procesar. 
        fecha: indica el mes y año en formato mm-aaaa. 

    Returns: 
        Devuelve una tupla (A,B,C)
        A: total de noticias del mes. 
        B: cantidad noticias EPU del mes. 
        C: diccionario con la cantidad de noticias EPU por categoría. 
    """
    total_news_month = 0
    epu_news_month = 0
    
    dict_category_epu_news = {
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
        total_news_month, epu_news_month = process_news_el_pais(year, month, terms_bag, dict_category_epu_news)

    elif (newspaper == "el_observador"):
        total_news_month, epu_news_month = process_news_el_observador(year, month, terms_bag, dict_category_epu_news)

    elif (newspaper == "la_diaria"):
        total_news_month, epu_news_month = process_news_la_diaria(year, month, terms_bag, dict_category_epu_news)
        
    elif (newspaper == "la_republica"):
        total_news_month, epu_news_month = process_news_la_republica(year, month, terms_bag, dict_category_epu_news)

    return total_news_month, epu_news_month, dict_category_epu_news
