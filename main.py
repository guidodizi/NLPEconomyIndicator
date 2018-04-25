# -*- coding: utf-8 -*-
import json
from indicador_incertidumbre import *

with open('bag_of_words.json') as data_file:
    bag_of_words = json.load(data_file)

not_ok = True
newspaper = ""
print u"Bienvenido al Indicador de Incertidumbre Economica para Uruguay \n " 
print u"1 - El Observador" 
print u"2 - El Pais" 
print u"3 - La Diaria" 
print u"4 - La República" 
print u"5 - Todos"  
mode = input("Ingrese el numero correspondiente al diario que desea: ")
while not_ok:
    if mode == 1:
        newspaper = "el_observador"
        not_ok = False
    elif mode == 2:
        newspaper = "el_pais"
        not_ok = False
    elif mode == 3:
        newspaper = "la_diaria"
        not_ok = False
    elif mode == 4:
        newspaper = "la_republica"
        not_ok = False
    else:
        print "\nValor invalido\n"
        print u"Bienvenido al Indicador de Incertidumbre Economica para Uruguay \n " 
        print u"1 - El Observador" 
        print u"2 - El Pais" 
        print u"3 - La Diaria" 
        print u"4 - La República" 
        print u"5 - Todos"  
        mode = input("Ingrese el numero correspondiente al diario que desea: ")


year  = input ("Ahora inngrese el anio que desea utilizar: ")
month  = input ("Ahora inngrese el mes que desea utilizar, siendo enero el 1 y todos el 13: ")

print(u"Se esta obteniendo el indicador de incertidumbre económica para el diario " + newspaper + " en el anio " + str(year) + " y el mes " + str(month))

news_qty_month, news_epu_month, qty_by_category = monthly_indicator_by_category(newspaper, year, month, bag_of_words)

print ("La cantidad de articulos total es: " + str(news_qty_month))
print ("La cantidad de articulos con EPU es: " + str(news_epu_month)) 
for key, value in qty_by_category.items():
    print (u"La cantidad de articulos de la categoría " + key + " es: " + str(value))

