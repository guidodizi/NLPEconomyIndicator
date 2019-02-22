# -*- coding: utf-8 -*-
import json
import sys
import quantity_date
import csv
import numpy as np
from datetime import datetime

import results_file_handler
import settings

# HELPER METHODS
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


def display_topics(model, feature_names, no_top_words):
    f= open("terms.txt","w+")
    for topic_idx, topic in enumerate(model.components_):
        
        print ("Topic %d:" % (topic_idx))
        print (" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))
        f.write("Topic %d:" % (topic_idx))
        f.write(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))
        f.write("\n")


def create_quantity_list():
    quantity_list = []
    date_from = settings.FULL_DATE['datefrom']
    date_to = settings.FULL_DATE['dateto']
    date_iter = month_year_iter(date_from, date_to)

    for date in date_iter: 
        year, month = date[0], date[1]
        date = quantity_date.Quantity_Date(month, year, settings.NO_TOPICS)  
        quantity_list.append(date)
    return quantity_list            


def write_csv_file_step1(quantiy_list):
    filepath = settings.STEP2_FILEPATH
    base_data = ["date", "epu_index"]

    for i in range(0,settings.NO_TOPICS):        
        base_data.append("Tema " + str(i))

    with open(filepath, 'w', encoding='utf-8', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)        
        wr.writerow(base_data)        
        for item in quantiy_list:
            row_data = [str(item.Month)+ '-' + str(item.Year), sum(item.Topics)]
            row_data = row_data + item.Topics
            wr.writerow(row_data)


#STEP 2
#TODO dividir entre la cantidad de noticias por mes
#STEP 3 
def scale_to_unit_standard_deviation():
    previous_results_path = settings.STEP2_FILEPATH
    filepath = settings.STEP3_FILEPATH
    results_file_handler.create_step3_results_file()

    step2_matrix = np.loadtxt(open(previous_results_path, "rb"),
                              delimiter=",", usecols=range(1, settings.NO_TOPICS + 2), skiprows=1)

    std_dev_dict = {}
    for i in range(len(step2_matrix[0])):
        step2_index = step2_matrix[:, i]
        std_dev = np.std(step2_index, dtype=np.float64)
        std_dev_dict[i] = std_dev

    with open(previous_results_path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        next(csvreader)  # Skips headers row                
        for row in csvreader:
            cols = len(row)
            date = row[0]

            col_data = [date]
            for i in range(1, cols):
                col_data.append(row[i]/std_dev_dict[i-1])  

            results_file_handler.append_csv_file_row(filepath, col_data)


#STEP 4
def scale_to_100_mean():
    previous_results_path = settings.STEP3_FILEPATH
    filepath = settings.RESULT_FILEPATH
    results_file_handler.create_epu_index_file()

    step4_matrix = np.loadtxt(open(previous_results_path, "rb"),
                              delimiter=",", usecols=range(1,settings.NO_TOPICS + 2), skiprows=1)    

    mean_coef_dict = {}
    for i in range(len(step4_matrix[0])):
        step4_index = step4_matrix[:, i]
        mean = np.mean(step4_index, dtype=np.float64)
        coef = (100 / mean)
        mean_coef_dict[i] = coef

    with open(previous_results_path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        next(csvreader)  # Skips headers row
        for row in csvreader:
            date = row[0]
            data = [date]

            for i in range(1, settings.NO_TOPICS):
                data.append(row[i]*mean_coef_dict[i-1])

            results_file_handler.append_csv_file_row(filepath, data)
