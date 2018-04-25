# -*- coding: utf-8 -*-
import json
from indicador_incertidumbre import *

with open('bag_of_words.json') as data_file:
    bag_of_words = json.load(data_file)

news_qty_month, news_epu_month, qty_by_category = monthly_indicator_by_category("la_republica", "", bag_of_words)

print ("La cantidad de articulos total es: " + str(news_qty_month))
print ("La cantidad de articulos con EPU es: " + str(news_epu_month)) 
for key, value in qty_by_category.items():
    print (u"La cantidad de articulos de la categoría " + key + " es: " + str(value))

