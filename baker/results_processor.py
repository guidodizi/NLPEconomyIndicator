# -*- coding: utf-8 -*-
import csv
from datetime import date
from datetime import timedelta
import json
import os

def get_initial_date():
    with open('date_ranges.json') as data_file:
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
    with open('date_ranges.json') as data_file:
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

def delete_epu_index():
    filepath = "results/epu_index.csv"
    try:
        os.remove(filepath)
    except OSError:
        pass

def generate_epu_index():
    delete_epu_index()
    
    filepath = "results/epu_index.csv"
    initial_date = get_initial_date()
    last_date = get_last_date()

    # Populate csv headers
    base_data = ["date", "epu_index", "epu_cat2_index", "epu_cat3_index", "epu_cat4_index", "epu_cat5_index",  "epu_cat6_index",
                "epu_cat7_index", "epu_cat8_index", "epu_cat9_index", "epu_cat10_index", "epu_cat11_index", "epu_cat12_index", 
                "epu_cat13_index", "epu_cat14_index"]
    with open(filepath, 'w', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(base_data)
    
    # Iterate over monthly results
    current_date = initial_date
    while current_date < last_date:      
        date = current_date.strftime("%m-%Y")

        # TODO: abrir los .csv de results y hacer el calculo

        epu_index_month = 100
        epu_cat2_index_month = 18
        epu_cat3_index_month = 18
        epu_cat4_index_month = 18
        epu_cat5_index_month = 18
        epu_cat6_index_month = 18
        epu_cat7_index_month = 18
        epu_cat8_index_month = 18
        epu_cat9_index_month = 18
        epu_cat10_index_month = 18
        epu_cat11_index_month = 18
        epu_cat12_index_month = 18
        epu_cat13_index_month = 18
        epu_cat14_index_month = 18

        data = [date, epu_index_month, epu_cat2_index_month, epu_cat3_index_month, epu_cat4_index_month,
            epu_cat5_index_month, epu_cat6_index_month, epu_cat7_index_month, epu_cat8_index_month, epu_cat9_index_month,
            epu_cat10_index_month, epu_cat11_index_month, epu_cat12_index_month, epu_cat13_index_month, epu_cat14_index_month]
            
        with open(filepath, 'a', newline='') as data_file:
            wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(data)

        current_date = add_one_month(current_date)


# MAIN
generate_epu_index()
