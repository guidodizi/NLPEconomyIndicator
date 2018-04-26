# -*- coding: utf-8 -*-
import json
from monthly_index import *

# AUXILIAR METHODS
def print_presentation():
    print (u"\n---------------------------------------------------------------")
    print (u"---------------------------------------------------------------")
    print (u"Bienvenido al Indicador de Incertidumbre Económica para Uruguay")

def newspaper_input_options():
    print (u"\nIndique la opción del diario que desea procesar.")
    print (u"  1 - El Observador")
    print (u"  2 - El País")
    print (u"  3 - La Diaria")
    print (u"  4 - La República")
    print (u"  S - Salir\n")
    return input("Opción: ")

def year_input_options():
    print (u"\nIndique el año que desea procesar.")
    print (u"  aaaa - Año exacto (ej. 2014)")
    print (u"  T - Todos")
    print (u"  S - Salir\n")
    return input("Opción: ")

def month_input_options():
    print (u"\nIndique el mes que desea procesar.")
    print (u"  mm - Mes exacto (ej. 01 es Enero)")
    print (u"  T - Todos")
    print (u"  S - Salir\n")
    return input("Opción: ")

def print_processing_message(newspaper, year, month):
    print(u"\nSe está obteniendo el Indicador de Incertidumbre Económica para:")
    if (newspaper == "el_observador"):
        print(u"  - Diario: El Observador")
    elif (newspaper == "el_pais"):
        print(u"  - Diario: El País")
    elif (newspaper == "la_diaria"):
        print(u"  - Diario: La Diaria")
    elif (newspaper == "la_republica"):
        print(u"  - Diario: La República")
    if (year == ""):
        print(u"  - Año: Todos")
    else:
        print(u"  - Año: " + str(year))
    if (month == ""):
        print(u"  - Mes: Todos")
    else:
        print(u"  - Mes: " + str(month))
    print(u"\nAguarde unos instantes...")

def is_integer(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def newspaper_input_section():
    input_ok = False
    newspaper = ""
    input_newspaper = newspaper_input_options()
    while not input_ok:
        if input_newspaper == "S" or input_newspaper == "s":
            exit()
        elif input_newspaper == "1":
            newspaper = "el_observador"
            input_ok = True
        elif input_newspaper == "2":
            newspaper = "el_pais"
            input_ok = True
        elif input_newspaper == "3":
            newspaper = "la_diaria"
            input_ok = True
        elif input_newspaper == "4":
            newspaper = "la_republica"
            input_ok = True
        else:
            print ("\nOpción inválida.\n")
            input_newspaper = newspaper_input_options()
    return newspaper

def year_input_section():
    input_ok = False
    year = ""
    input_year = year_input_options()
    while not input_ok:
        if input_year == "S" or input_year == "s":
            exit()
        elif input_year == "T" or input_year == "t":
            year = ""
            input_ok = True
        elif len(input_year) == 4 and is_integer(input_year):
            year = input_year
            input_ok = True
        else:
            print ("\nOpción inválida.\n")
            input_year = year_input_options()
    return year

def month_input_section():
    input_ok = False
    month = ""
    input_month = month_input_options()
    while not input_ok:
        if input_month == "S" or input_month == "s":
            exit()
        elif input_month == "T" or input_month == "t":
            month = ""
            input_ok = True
        elif len(input_month) == 2 and is_integer(input_month):
            month = input_month
            input_ok = True
        else:
            print ("\nOpción inválida.\n")
            input_month = month_input_options()
    return month


# MAIN
with open('terms.json') as data_file:
    terms_bag = json.load(data_file)

print_presentation()

# Input sections
newspaper = newspaper_input_section()
year = year_input_section()
month = month_input_section()

print_processing_message(newspaper, year, month)

# Execute news processing
total_news_month, epu_news_month, dict_category_epu_news = monthly_indicator_by_category(newspaper, year, month, terms_bag)

#Print reults
print ("La cantidad de articulos total es: " + str(total_news_month))
print ("La cantidad de articulos con EPU es: " + str(epu_news_month))
for key, value in dict_category_epu_news.items():
    print (u"La cantidad de articulos de la categoría " + key + " es: " + str(value))
