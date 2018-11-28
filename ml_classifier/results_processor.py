# -*- coding: utf-8 -*-
import csv
import json
import os
import sys

import numpy as np
import pandas as pd

import results_file_handler
import settings
from helper_methods import *


def scale_to_relative_count(newspaper):
    print(u"\nProcesamiento de noticias finalizado.")
    print(u"\nAguarde mientras se normalizan los resultados ...")
    previous_results_path = settings.STEP_1_2_3_FILEPATH.format("1", newspaper)
    filepath = settings.STEP_1_2_3_FILEPATH.format("2", newspaper)
    results_file_handler.create_step2_results_file(newspaper)
    with open(previous_results_path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        next(csvreader) # Skips headers row
        for row in csvreader:
            cols = len(row)
            date = row[1]
            total_news_month = int(row[2])
            if (total_news_month == 0):
                total_news_month = 1 # To avoid division by 0

            col_data = [newspaper, date]
            for i in range(3, cols):
                col_data.append(row[i]/total_news_month)

            results_file_handler.append_csv_file_row(filepath, col_data)


def scale_to_unit_standard_deviation(newspaper):
    previous_results_path = settings.STEP_1_2_3_FILEPATH.format("2", newspaper)
    filepath = settings.STEP_1_2_3_FILEPATH.format("3", newspaper)
    results_file_handler.create_step3_results_file(newspaper)

    step2_array = np.loadtxt(open(previous_results_path, "rb"), delimiter=",", usecols=range(2, 3), skiprows=1)
    std_dev = np.std(step2_array, dtype=np.float64)

    with open(previous_results_path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        next(csvreader) # Skips headers row
        for row in csvreader:
            date = row[1]
            std_value = (row[2]/std_dev)
            col_data = [newspaper, date, std_value]

            results_file_handler.append_csv_file_row(filepath, col_data)


def create_matrix_full_range(incomplete_matrix, range, date_to, date_from):
    first_year = int(date_from.split("-")[1])
    n_months = get_index_from_a_date(date_to, first_year)
    n_categories = 1

    zero_matrix = np.zeros(shape=(n_months, n_categories))
    zero_matrix[zero_matrix == 0] = -1
    i = 0
    for r in range:
        index = get_index_from_a_date(r, first_year)
        zero_matrix[index] = incomplete_matrix[i]
        i += 1
    return zero_matrix


def get_index_from_a_date(date, first_year):
    year = date.split("-")[1]
    month = date.split("-")[0]
    year_num = int(year) - first_year
    index = year_num * 12 + int(month) - 1
    return index


def generate_epu_index():
    # TODO: Chequear que haya archivos step3_results, sino indicar un mesaje de error
    average_newspaper_results()
    scale_to_100_mean()


def average_newspaper_results():
    directory = os.fsencode('results')

    date_from = settings.EPU_DATE_RANGE['datefrom']
    date_to = settings.EPU_DATE_RANGE['dateto']

    arrays = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv") and filename.startswith("ml_step3_results"):
            step3_array = np.loadtxt(open('results/' + filename, "rb"), delimiter=",", usecols=range(2, 3), skiprows=1)
            df = pd.read_csv('results/' + filename)
            date_ranges = df['date']
            if (date_ranges[df.index[0]] != date_from and date_ranges[df.index[-1]] != date_to):
                # TODO: ^^ check this if -> I changed the 'or' for 'and' because when newspapers range were equal then it generated a wrong matrix 
                step3_array = create_matrix_full_range(step3_array, date_ranges, date_to, date_from)
            arrays.append(step3_array)
            continue
        else:
            continue

    # TODO: change this average calculations for array instead of matrix
    average_array = arrays[0].copy()
    quant_arrays = len(arrays)
    rows = arrays[0].shape[0]
    columns = arrays[0].shape[1]
    x = 0
    while (x < rows):
        y = 0
        while (y < columns):
            i = 0
            sum_field = 0
            quant = 0
            while (i < quant_arrays):
                if (arrays[i][x][y] != -1):
                    sum_field += arrays[i][x][y]
                    quant += 1
                i += 1

            average = sum_field / quant
            average_array[x][y] = average
            y += 1
        x += 1

    # Write the results of the average of all arrays
    filepath = settings.STEP_4_FILEPATH
    results_file_handler.create_step4_results_average_file()
 
    # Iterate over the longest period
    month_date_from = int(date_from.split("-")[0])
    year_date_from = int(date_from.split("-")[1])
    date_from_str = str(month_date_from) + "-" + str(year_date_from)
    x = 0
    # TODO: change this for array instead of matrix
    while (date_from_str != date_to):
        data = ["Promedio", date_from_str]
        y = 0
        while y < average_array.shape[1]:
            data.append(average_array[x][y])
            y += 1

        with open(filepath, 'a', newline='') as data_file:
            wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(data)

        x += 1
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
    previous_results_path = settings.STEP_4_FILEPATH
    filepath = settings.EPU_INDEX_FILEPATH
    results_file_handler.create_epu_index_file()

    step4_array = np.loadtxt(open(previous_results_path, "rb"), delimiter=",", usecols=range(2, 3), skiprows=1)

    mean_coef_dict = {}
    # TODO: change this for array instead of matrix
    for i in range(len(step4_array[0])):
        step4_index = step4_array[:, i]
        mean = np.mean(step4_index, dtype=np.float64)
        coef = (100 / mean)
        mean_coef_dict[i] = coef

    with open(previous_results_path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        next(csvreader) # Skips headers row
        for row in csvreader:
            date = row[1]
            data = ["EPU Final", date]

            for i in range(2, 3):
                data.append(row[i]*mean_coef_dict[i-2])

            results_file_handler.append_csv_file_row(filepath, data)
