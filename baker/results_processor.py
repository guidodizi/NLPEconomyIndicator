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
    step2_matrix = np.loadtxt(open(previous_results_path, "rb"), delimiter=",", usecols=(2,3,4,5,6,7,8,9,10,11,12,13,14,15), skiprows=1)
    categories_count = len(step2_matrix[0])
    std_dev_dict = {}
    for i in range(categories_count):
        step2_index = step2_matrix[:,i]
        std_dev = np.std(step2_index, dtype=np.float64)
        std_dev_dict[i] = std_dev
    with open(previous_results_path, newline='') as csvfile:
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
