# -*- coding: utf-8 -*-
import csv
import json
import os
from datetime import date

import settings


def append_csv_file_row(filepath, data):
    with open(filepath, 'a', encoding='utf-8', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(data)


def write_csv_file_row(filepath, data):
    with open(filepath, 'w', encoding='utf-8', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(data)


def create_step1_results_file():
    filepath = settings.STEP1_FILEPATH    
    base_data = ["date", "epu_index"]

    for i in range(0,settings.NO_TOPICS):        
        base_data.append("Tema " + str(i))

    write_csv_file_row(filepath, base_data)


def create_step2_results_file():
    filepath = settings.STEP2_FILEPATH
    base_data = ["date", "epu_index_rel"]

    for i in range(0, settings.NO_TOPICS):        
        base_data.append("Tema_rel " + str(i))

    write_csv_file_row(filepath, base_data)


def create_step3_results_file():
    filepath = settings.STEP3_FILEPATH
    base_data = ["date", "epu_index_rel"]

    for i in range(0, settings.NO_TOPICS):        
        base_data.append("Tema_std " + str(i))

    write_csv_file_row(filepath, base_data)


def create_epu_index_file():
    filepath = settings.RESULT_FILEPATH
    base_data = ["date", "epu_uruguay"]

    for i in range(0, settings.NO_TOPICS):
        base_data.append("Tema_std " + str(i))

    write_csv_file_row(filepath, base_data)
