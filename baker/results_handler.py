# -*- coding: utf-8 -*-
import csv
import os

def delete_results_file(newspaper):   
    filepath = "results/results_" + newspaper + ".csv"
    try:
        os.remove(filepath)
    except OSError:
        pass

def create_results_file(newspaper):
    filepath = "results/results_" + newspaper + ".csv"
    base_data = ["newspaper", "date", "total_news", "epu_news", "epu_cat2_news", "epu_cat3_news", "epu_cat4_news", "epu_cat5_news", 
                "epu_cat6_news", "epu_cat7_news", "epu_cat8_news", "epu_cat9_news", "epu_cat10_news", "epu_cat11_news", "epu_cat12_news", 
                "epu_cat13_news", "epu_cat14_news"]
    with open(filepath, 'w', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(base_data)

def save_results(newspaper, month, year, total_news_month, epu_news_month, dict_category_epu_news):
    filepath = "results/results_" + newspaper + ".csv"
    date = str(month) + "-" + str(year)
    data = [newspaper, date, total_news_month, epu_news_month, dict_category_epu_news['2'], dict_category_epu_news['3'],
            dict_category_epu_news['4'], dict_category_epu_news['5'], dict_category_epu_news['6'], dict_category_epu_news['7'],
            dict_category_epu_news['8'], dict_category_epu_news['9'], dict_category_epu_news['10'], dict_category_epu_news['11'],
            dict_category_epu_news['12'], dict_category_epu_news['13'], dict_category_epu_news['14']]
    with open(filepath, 'a', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(data)
