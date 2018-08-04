# -*- coding: utf-8 -*-
import csv
import json
import os
import sys

import numpy as np

import results_file_handler
import settings
from helper_methods import *


def scale_to_relative_count(newspaper):
    previous_results_path = settings.STEP_1_2_3_FILEPATH.format("1", newspaper)
    filepath = settings.STEP_1_2_3_FILEPATH.format("2", newspaper)
    results_file_handler.create_step2_results_file(newspaper)
    with open(previous_results_path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        next(csvreader)  # Skips headers row
        for row in csvreader:
            cols = len(row)
            date = row[1]
            count = int(row[2])
            if (count == 0):
                count = 1  # To avoid division by 0

            col_data = [newspaper, date]
            for i in range(3, cols):
                col_data.append(row[i]/count)

            results_file_handler.append_csv_file_row(filepath, col_data)


def scale_to_unit_standard_deviation(newspaper):
    print(u"\nProcesamiento de noticias finalizado.")
    print(u"\nAguarde mientras se normalizan los resultados ...")
    previous_results_path = settings.STEP_1_2_3_FILEPATH.format("2", newspaper)
    filepath = settings.STEP_1_2_3_FILEPATH.format("3", newspaper)
    results_file_handler.create_step3_results_file(newspaper)

    step2_matrix = np.loadtxt(open(previous_results_path, "rb"),
                              delimiter=",", usecols=range(2, settings.CATEGORIES_COUNT + 3), skiprows=1)

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
            date = row[1]

            col_data = [newspaper, date]
            for i in range(2, cols):
                col_data.append(row[i]/std_dev_dict[i-2])

            results_file_handler.append_csv_file_row(filepath, col_data)


def generate_epu_index():
     # TODO: implementar
    print("\nFalta implementación.\n")
    # 1) Chequear que haya archivos step3_results, sino indicar un mesaje de error
    # 2) average_newspaper_results()
    # 3) scale_to_100_mean()
    sys.exit()


def average_newspaper_results():
    # TODO: implementar
    print("\nFalta implementación.\n")
    filepath = settings.STEP_4_FILEPATH
    sys.exit()


def scale_to_100_mean():
    previous_results_path = settings.STEP_4_FILEPATH
    filepath = settings.EPU_INDEX_FILEPATH
    results_file_handler.create_epu_index_file()

    step4_matrix = np.loadtxt(open(previous_results_path, "rb"),
                              delimiter=",", usecols=(2, settings.CATEGORIES_COUNT + 3), skiprows=1)

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
            date = row[1]
            data = [date]

            for i in range(2, settings.CATEGORIES_COUNT):
                data.append(row[i]*mean_coef_dict[i-2])

            results_file_handler.append_csv_file_row(filepath, data)
