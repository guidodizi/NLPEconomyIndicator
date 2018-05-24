# -*- coding: utf-8 -*-
import csv
from datetime import date
from datetime import timedelta
import json
import os
import results_handler
import numpy as np

def scale_to_relative_count(newspaper):
    previous_results_path = "results/step1_results_" + newspaper + ".csv"
    filepath = "results/step2_results_" + newspaper + ".csv"
    results_handler.create_step2_results_file(newspaper)
    with open(previous_results_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        next(csvreader) # Skips headers row
        for row in csvreader:
            date = row[1]
            count = int(row[2])
            data = [newspaper, date, (row[3]/count), (row[4]/count), (row[5]/count), (row[6]/count), (row[7]/count),
                   (row[8]/count), (row[9]/count), (row[10]/count), (row[11]/count), (row[12]/count), (row[13]/count), 
                   (row[14]/count), (row[15]/count), (row[16]/count)]
            with open(filepath, 'a', newline='') as data_file:
                wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
                wr.writerow(data)

def scale_to_unit_standard_deviation(newspaper):
    previous_results_path = "results/step2_results_" + newspaper + ".csv"
    filepath = "results/step3_results_" + newspaper + ".csv"
    results_handler.create_step3_results_file(newspaper)
    matrix = np.loadtxt(open(previous_results_path, "rb"), delimiter=",", usecols=(2,3,4,5,6,7,8,9,10,11,12,13,14,15), skiprows=1)
    #TODO: a partir de los resultados estos se debe hayar la desviacion estandar y hacer la division
    print(matrix)


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
