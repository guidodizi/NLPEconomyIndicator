# -*- coding: utf-8 -*-
import csv
import os
from datetime import date

def delete_results_files(newspaper):
    delete_step1_results_file(newspaper)
    delete_step2_results_file(newspaper)
    delete_step3_results_file(newspaper)

def delete_step1_results_file(newspaper):
    filepath = "results/step1_results_" + newspaper + ".csv"
    try:
        os.remove(filepath)
    except OSError:
        pass

def delete_step2_results_file(newspaper):
    filepath = "results/step2_results_" + newspaper + ".csv"
    try:
        os.remove(filepath)
    except OSError:
        pass

def delete_step3_results_file(newspaper):
    filepath = "results/step3_results_" + newspaper + ".csv"
    try:
        os.remove(filepath)
    except OSError:
        pass

def delete_epu_index_file():
    filepath = "results/epu_index.csv"
    try:
        os.remove(filepath)
    except OSError:
        pass

def create_step1_results_file(newspaper):
    filepath = "results/step1_results_" + newspaper + ".csv"
    base_data = ["newspaper", "date", "total_news", "epu_news", "epu_cat2_news", "epu_cat3_news", "epu_cat4_news", "epu_cat5_news", 
                "epu_cat6_news", "epu_cat7_news", "epu_cat8_news", "epu_cat9_news", "epu_cat10_news", "epu_cat11_news", "epu_cat12_news", 
                "epu_cat13_news", "epu_cat14_news"]
    with open(filepath, 'w', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(base_data)

def create_step2_results_file(newspaper):
    filepath = "results/step2_results_" + newspaper + ".csv"
    base_data = ["newspaper", "date", "epu_news_rel", "epu_cat2_news_rel", "epu_cat3_news_rel", "epu_cat4_news_rel", "epu_cat5_news_rel", 
                "epu_cat6_news_rel", "epu_cat7_news_rel", "epu_cat8_news_rel", "epu_cat9_news_rel", "epu_cat10_news_rel", "epu_cat11_news_rel", 
                "epu_cat12_news_rel", "epu_cat13_news_rel", "epu_cat14_news_rel"]
    with open(filepath, 'w', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(base_data)

def create_step3_results_file(newspaper):
    filepath = "results/step3_results_" + newspaper + ".csv"
    base_data = ["newspaper", "date", "epu_news_std", "epu_cat2_news_std", "epu_cat3_news_std", "epu_cat4_news_std", "epu_cat5_news_std", 
                "epu_cat6_news_std", "epu_cat7_news_std", "epu_cat8_news_std", "epu_cat9_news_std", "epu_cat10_news_std", "epu_cat11_news_std", 
                "epu_cat12_news_std", "epu_cat13_news_std", "epu_cat14_news_std"]
    with open(filepath, 'w', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(base_data)

def create_epu_index_file():
    filepath = "results/epu_index.csv"
    base_data = ["date", "epu_index", "epu_cat2_index", "epu_cat3_index", "epu_cat4_index", "epu_cat5_index",  "epu_cat6_index",
                "epu_cat7_index", "epu_cat8_index", "epu_cat9_index", "epu_cat10_index", "epu_cat11_index", "epu_cat12_index", 
                "epu_cat13_index", "epu_cat14_index"]
    with open(filepath, 'w', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(base_data)

def save_step1_results(newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news):
    filepath = "results/step1_results_" + newspaper + ".csv"
    this_date = date(year, month, 1)
    str_date = this_date.strftime("%m-%Y")
    data = [newspaper, str_date, total_news_month, epu_news_month, dict_category_epu_news['2'], dict_category_epu_news['3'],
            dict_category_epu_news['4'], dict_category_epu_news['5'], dict_category_epu_news['6'], dict_category_epu_news['7'],
            dict_category_epu_news['8'], dict_category_epu_news['9'], dict_category_epu_news['10'], dict_category_epu_news['11'],
            dict_category_epu_news['12'], dict_category_epu_news['13'], dict_category_epu_news['14']]
    with open(filepath, 'a', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(data)
