# -*- coding: utf-8 -*-
import json
import sys
from datetime import datetime

import settings

# HELPER METHODS

# ----- Input -----

def input_options_message():
    print(u"\nIndique la operación a realizar:")
    print(u"  1 - Procesar \"El Observador\"")
    print(u"  2 - Procesar \"La Diaria\"")
    print(u"  3 - Procesar \"Búsqueda\"")
    print(u"  G - Generar indicador a partir de los diarios ya procesados")
    print(u"  S - Salir\n")
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
            option = settings.NEWSPAPERS["el_observador"]["id"]
            input_ok = True
        elif input_opt == "2":
            option = settings.NEWSPAPERS["la_diaria"]["id"]
            input_ok = True
        elif input_opt == "3":
            option = settings.NEWSPAPERS["busqueda"]["id"]
            input_ok = True
        else:
            print("\nOpción inválida.\n")
            input_opt = input_options_message()
    return option


# ----- Console Logging -----

def print_presentation():
    print(u"\n---------------------------------------------------------------")
    print(u"---------------------------------------------------------------")
    print(u"Bienvenido al Indicador de Incertidumbre Económica para Uruguay")


def print_processing_message(newspaper):
    print(u"\nSe está obteniendo el Indicador de Incertidumbre Económica para:")
    if (newspaper == "el_observador"):
        print(u"  - Diario: El Observador")
    elif (newspaper == "la_diaria"):
        print(u"  - Diario: La Diaria")
    elif (newspaper == "busqueda"):
        print(u"  - Semanario: Búsqueda")
    print(u"\nAguarde unos instantes...")


def print_finish():
    print(u"\n¡Procesamiento finalizado!")
    print(u"Puede ver los resultados en la carpeta \"/baker/results\" \n")


# ----- Auxiliar -----

def month_year_iter(date_from, date_to):
    start_month = int(date_from.split("-")[0])
    start_year = int(date_from.split("-")[1])
    end_month = int(date_to.split("-")[0])
    end_year = int(date_to.split("-")[1])
    ym_start = 12 * start_year + start_month - 1
    ym_end = 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m+1


def load_categories_dictionary():
    dict_category_epu_news = {}
    total_categories = settings.CATEGORIES_COUNT
    for i in range(2, total_categories + 2):
        dict_category_epu_news[str(i)] = 0
    return dict_category_epu_news
