# -*- coding: utf-8 -*-
import json
import sys
from datetime import datetime

# HELPER METHODS

# ----- Input -----
def input_options_message():
    print (u"\nIndique la operación a realizar:")
    print (u"  1 - Procesar \"La República\"")
    print (u"  2 - Procesar \"El Observador\"")
    print (u"  3 - Procesar \"La Diaria\"")
    print (u"  4 - Procesar \"Búsqueda\"")
    print (u"  G - Generar indicador a partir de los diarios ya procesados")
    print (u"  S - Salir\n")
    return input("Opción: ")

def options_input_section():
    input_ok = False
    option = ""
    input_opt = input_options_message()
    while not input_ok:
        if input_opt == "S" or input_opt == "s":
            exit()
        elif input_opt == "G" or input_opt == "g":
            option = "generar_epu"
            input_ok = True
        elif input_opt == "1":
            option = "la_republica"
            input_ok = True
        elif input_opt == "2":
            option = "el_observador"
            input_ok = True
        elif input_opt == "3":
            option = "la_diaria"
            input_ok = True
        elif input_opt == "4":
            option = "busqueda"
            input_ok = True
        else:
            print ("\nOpción inválida.\n")
            input_opt = input_options_message()
    return option

# ----- Console Logging -----
def print_presentation():
    print (u"\n---------------------------------------------------------------")
    print (u"---------------------------------------------------------------")
    print (u"Bienvenido al Indicador de Incertidumbre Económica para Uruguay")

def print_processing_message(newspaper):
    print(u"\nSe está obteniendo el Indicador de Incertidumbre Económica para:")
    if (newspaper == "el_observador"):
        print(u"  - Diario: El Observador")
    elif (newspaper == "la_diaria"):
        print(u"  - Diario: La Diaria")
    elif (newspaper == "la_republica"):
        print(u"  - Diario: La República")
    elif (newspaper == "busqueda"):
        print(u"  - Semanario: Búsqueda")
    print(u"\nAguarde unos instantes...")

def print_finish():
    print (u"\n¡Procesamiento finalizado!")
    print (u"Puede ver los resultados en la carpeta \"/baker/results\" \n")

# ----- Auxiliar -----
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
    dict_category_epu_news = {}
    total_categories = categories_count()
    for i in range(2, total_categories + 2):
        dict_category_epu_news[str(i)] = 0
    return dict_category_epu_news

def categories_count():
    with open('terms.json', 'r+', encoding='utf-8') as data_file:
        terms_bag = json.load(data_file)
    count = len(terms_bag['terms']) - 2
    return count

# def news_date_range(newspaper):
#     date_range = {
#         'datefrom': 15,
#         'dateto': 10
#     }
#     return date_range

# def epu_index_date_range():
#     date_range = {
#         'datefrom': 15,
#         'dateto': 10
#     }
#     return date_range

# def get_initial_date():
#     with open('date_ranges.json', 'r+', encoding='utf-8') as data_file:
#         date_ranges = json.load(data_file)
#     initial_date = date.max
#     for date_range in date_ranges['ranges']:
#         date_from = date_range['datefrom']
#         month_from = int(date_from.split("-")[0])
#         year_from = int(date_from.split("-")[1])
#         this_date = date(year_from, month_from, 1)
#         if this_date < initial_date:
#             initial_date = this_date
#     return initial_date

# def get_last_date():
#     with open('date_ranges.json', 'r+', encoding='utf-8') as data_file:
#         date_ranges = json.load(data_file)
#     last_date = date.min
#     for date_range in date_ranges['ranges']:
#         date_to = date_range['dateto']
#         month_from = int(date_to.split("-")[0])
#         year_from = int(date_to.split("-")[1])
#         this_date = date(year_from, month_from, 1)
#         if this_date > last_date:
#             last_date = this_date
#     return last_date

# def add_one_month(dt0):
#     dt1 = dt0.replace(day=1)
#     dt2 = dt1 + timedelta(days=32)
#     dt3 = dt2.replace(day=1)
#     return dt3
