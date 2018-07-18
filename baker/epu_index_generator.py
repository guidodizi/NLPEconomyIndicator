# -*- coding: utf-8 -*-
import csv
from datetime import date
from datetime import timedelta
import json
import os
import results_handler
import numpy as np

def get_initial_date():
    with open('date_ranges.json', 'r+', encoding='utf-8') as data_file:
        date_ranges = json.load(data_file)
    initial_date = date.max
    for date_range in date_ranges['ranges']:
        date_from = date_range['datefrom']
        month_from = int(date_from.split("-")[0])
        year_from = int(date_from.split("-")[1])
        this_date = date(year_from, month_from, 1)
        if this_date < initial_date:
            initial_date = this_date
    return initial_date

def get_last_date():
    with open('date_ranges.json', 'r+', encoding='utf-8') as data_file:
        date_ranges = json.load(data_file)
    last_date = date.min
    for date_range in date_ranges['ranges']:
        date_to = date_range['dateto']
        month_from = int(date_to.split("-")[0])
        year_from = int(date_to.split("-")[1])
        this_date = date(year_from, month_from, 1)
        if this_date > last_date:
            last_date = this_date
    return last_date

def add_one_month(dt0):
    dt1 = dt0.replace(day=1)
    dt2 = dt1 + timedelta(days=32)
    dt3 = dt2.replace(day=1)
    return dt3


# MAIN
# TODO: 
# 1) obtener todos los archivos que empiecen con "step3_"
# 2) para cada mes y cada categoria epu calcular el valor promedio entre los diarios -> generar archivo
# 3) a partir del archivo anterior, normalizar los resultados multiplicando para que la media tenga valor 100 -> generar archivo final "epu_index.csv"
