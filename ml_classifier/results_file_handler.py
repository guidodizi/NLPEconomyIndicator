# -*- coding: utf-8 -*-
import csv
import json
import os
from datetime import date

import settings


def delete_results_files(newspaper):
    for step in range(1, 4):
        filepath = settings.STEP_1_2_3_FILEPATH.format(str(step), newspaper)
        delete_file(filepath)


def delete_results_average_file():
    filepath = settings.STEP_4_FILEPATH
    delete_file(filepath)


def delete_epu_index_file():
    filepath = settings.EPU_INDEX_FILEPATH
    delete_file(filepath)


def delete_file(filepath):
    try:
        os.remove(filepath)
    except OSError:
        pass


def write_csv_file_row(filepath, data):
    with open(filepath, 'w', encoding='utf-8', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(data)


def append_csv_file_row(filepath, data):
    with open(filepath, 'a', encoding='utf-8', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(data)


def create_step1_results_file(newspaper):
    filepath = settings.STEP_1_2_3_FILEPATH.format("1", newspaper)
    base_data = ["newspaper", "date", "total_news", "epu_news_count"]
    write_csv_file_row(filepath, base_data)


def create_step2_results_file(newspaper):
    filepath = settings.STEP_1_2_3_FILEPATH.format("2", newspaper)
    base_data = ["newspaper", "date", "epu_news_rel"]
    write_csv_file_row(filepath, base_data)


def create_step3_results_file(newspaper):
    filepath = settings.STEP_1_2_3_FILEPATH.format("3", newspaper)
    base_data = ["newspaper", "date", "epu_news_std"]
    write_csv_file_row(filepath, base_data)


def create_step4_results_average_file():
    filepath = settings.STEP_4_FILEPATH
    base_data = ["newspaper", "date", "epu_news_avg"]
    write_csv_file_row(filepath, base_data)


def create_epu_index_file():
    filepath = settings.EPU_INDEX_FILEPATH
    base_data = ["newspaper", "date", "epu_uruguay"]
    write_csv_file_row(filepath, base_data)


def save_step1_results(newspaper, month, year, total_news_month, epu_news_month):
    filepath = settings.STEP_1_2_3_FILEPATH.format("1", newspaper)
    this_date = date(year, month, 1)
    str_date = this_date.strftime("%m-%Y")
    data = [newspaper, str_date, total_news_month, epu_news_month]
    append_csv_file_row(filepath, data)
