# -*- coding: utf-8 -*-
import csv
from datetime import date
from datetime import timedelta
import json
import os
import results_handler
import numpy as np
import pandas as pd

def scale_to_relative_count(newspaper):
    previous_results_path = "results/step1_results_" + newspaper + ".csv"    
    filepath = "results/step2_results_" + newspaper + ".csv"
    results_handler.create_step2_results_file(newspaper)
    with open(previous_results_path, 'r+', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        next(csvreader) # Skips headers row
        for row in csvreader:
            date = row[1]
            count = int(row[2])
            if (count == 0):
                count = 1
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
    step2_matrix = np.loadtxt(open(previous_results_path, "rb"), delimiter=",", usecols=(2,3,4,5,6,7,8,9,10,11,12,13,14,15), skiprows=1)
    categories_count = len(step2_matrix[0])
    std_dev_dict = {}
    for i in range(categories_count):
        step2_index = step2_matrix[:,i]
        std_dev = np.std(step2_index, dtype=np.float64)
        std_dev_dict[i] = std_dev
    with open(previous_results_path, 'r+', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        next(csvreader) # Skips headers row
        for row in csvreader:
            date = row[1]
            data = [newspaper, date, (row[2]/std_dev_dict[0]), (row[3]/std_dev_dict[1]), (row[4]/std_dev_dict[2]), (row[5]/std_dev_dict[3]), 
                    (row[6]/std_dev_dict[4]), (row[7]/std_dev_dict[5]), (row[8]/std_dev_dict[6]), (row[9]/std_dev_dict[7]), 
                    (row[10]/std_dev_dict[8]), (row[11]/std_dev_dict[9]), (row[12]/std_dev_dict[10]),  (row[13]/std_dev_dict[11]), 
                    (row[14]/std_dev_dict[12]), (row[15]/std_dev_dict[13])]
            with open(filepath, 'a', newline='') as data_file:
                wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
                wr.writerow(data)

def create_matrix_full_range(incomplete_matrix,range, date_to, date_from):
    

    first_year = int(date_from.split("-")[1])       
    cant_months =  get_index_from_a_date(date_to,first_year)
    cant_categories = 14
        
    zero_matrix = np.zeros(shape=(cant_months,cant_categories))
    zero_matrix[zero_matrix == 0] = -1
    i = 0   
    for r in range:        
        index = get_index_from_a_date(r,first_year)
        zero_matrix[index] = incomplete_matrix[i] 
        i += 1
    return zero_matrix

def get_index_from_a_date(date, first_year):
    year = date.split("-")[1]
    month = date.split("-")[0]    
    year_num = int(year) - first_year
    index = year_num * 12 + int(month) - 1
    return index

def join_newspaper_results_with_average():
    directory = os.fsencode('results')
    
        # check the shape of the matrix to create identical to "el observador"
    with open('date_ranges.json', 'r+') as data_file:
        date_ranges = json.load(data_file)
    for dr in date_ranges['ranges']:        
        if (dr['newspaper'] == "el_observador"):
            date_from = dr['datefrom']
            date_to = dr['dateto']

    matrixes = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)       
        if filename.endswith(".csv") and filename.startswith("step3_results"):                                 
            step3_matrix = np.loadtxt(open('results/' + filename, "rb"), delimiter=",", usecols=(2,3,4,5,6,7,8,9,10,11,12,13,14,15), skiprows=1)
            df = pd.read_csv('results/' + filename)
            date_ranges = df['date']                    
            if (date_ranges[df.index[0]] != '01-2002'):
                step3_matrix = create_matrix_full_range(step3_matrix, date_ranges, date_to, date_from)                
            matrixes.append(step3_matrix)
            continue
        else:
            continue
    
    average_matrix = matrixes[0].copy()
    quant_matrixes = len(matrixes)      
    rows = matrixes[0].shape[0]
    columns = matrixes[0].shape[1]
    x = 0    
    while (x < rows):
        y = 0
        while (y < columns):                        
            i = 0
            sum_field = 0
            quant = 0 
            while (i < quant_matrixes):
                if (matrixes[i][x][y] != -1):
                    sum_field += matrixes[i][x][y]
                    quant += 1
                i += 1
            average = sum_field / quant
            average_matrix[x][y] = average    
            y += 1                     
        x += 1

    #write the results of the average of all matrixes    
    filepath = "results/step4_results_average.csv"
    results_handler.create_step4_results_file("average")
    i = 0 
    #recorrer todos el rango de fecha del observador
    month_date_from = int(date_from.split("-")[0])
    year_date_from = int(date_from.split("-")[1])
    date_from_str = str(month_date_from) + "-" + str(year_date_from)    
    while (date_from_str != date_to):          
        data = ["average", date_from_str, average_matrix[i][0], average_matrix[i][1], average_matrix[i][2], average_matrix[i][3], average_matrix[i][4],
                average_matrix[i][5], average_matrix[i][6], average_matrix[i][7], average_matrix[i][8], average_matrix[i][9], average_matrix[i][10],
                average_matrix[i][11], average_matrix[i][12], average_matrix[i][13]]                  
        with open(filepath, 'a', newline='') as data_file:
            wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(data)
        i += 1
        if month_date_from == 12:
            month_date_from = 1
            year_date_from += 1
        else:
            month_date_from += 1
        if (month_date_from < 10):
            date_from_str = "0" + str(month_date_from) + "-" + str(year_date_from)   
        else:
            date_from_str = str(month_date_from) + "-" + str(year_date_from)            
    
def scale_to_100_mean():
    # TODO: esto en realidad se debe hacer una vez que ya se mezclaron todos los diarios en un solo indicador, y genera el EPU definitivo
    previous_results_path = "results/step4_results_average.csv"
    filepath = "results/step5_results_final.csv"
    results_handler.create_step5_results_file("final")
    step3_matrix = np.loadtxt(open(previous_results_path, "rb"), delimiter=",", usecols=(2,3,4,5,6,7,8,9,10,11,12,13,14,15), skiprows=1)
    categories_count = len(step3_matrix[0])
    mean_coef_dict = {}
    for i in range(categories_count):
        step3_index = step3_matrix[:,i]
        mean = np.mean(step3_index, dtype=np.float64)
        coef = (100 / mean)
        mean_coef_dict[i] = coef
    with open(previous_results_path, 'r+', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        next(csvreader) # Skips headers row
        for row in csvreader:
            date = row[1]
            data = ["final", date, (row[2]*mean_coef_dict[0]), (row[3]*mean_coef_dict[1]), (row[4]*mean_coef_dict[2]), (row[5]*mean_coef_dict[3]), 
                    (row[6]*mean_coef_dict[4]), (row[7]*mean_coef_dict[5]), (row[8]*mean_coef_dict[6]), (row[9]*mean_coef_dict[7]), 
                    (row[10]*mean_coef_dict[8]), (row[11]*mean_coef_dict[9]), (row[12]*mean_coef_dict[10]),  (row[13]*mean_coef_dict[11]), 
                    (row[14]*mean_coef_dict[12]), (row[15]*mean_coef_dict[13])]
            with open(filepath, 'a', newline='') as data_file:
                wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
                wr.writerow(data)
