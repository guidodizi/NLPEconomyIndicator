# -*- coding: utf-8 -*-
import json
from datetime import date
from datetime import datetime

# FOR GLOBAL VARIABLES AND DATA


def init():
    global STEP_1_2_3_FILEPATH
    global STEP_4_FILEPATH
    global EPU_INDEX_FILEPATH
    global NEWS_JSON_FILEPATH
    global NEWS_XML_FILEPATH
    global NEWS_COUNT_FILEPATH
    global TERMS_BAG
    global NEWSPAPERS
    global CATEGORIES_COUNT
    global COLUMNS_COUNT_1
    global COLUMNS_COUNT_2
    global COLUMNS_COUNT_3
    global EPU_DATE_RANGE

    STEP_1_2_3_FILEPATH = "results/step{0}_results_{1}.csv"
    STEP_4_FILEPATH = "results/step4_results_average.csv"
    EPU_INDEX_FILEPATH = "results/epu_index_uruguay.csv"
    NEWS_JSON_FILEPATH = "../news/{0}/{1}/{2}/data.json"
    NEWS_XML_FILEPATH = "../news/{0}/{1}/{2}/{0}.xml"
    NEWS_COUNT_FILEPATH = "../news/{0}/cant_noticias_{0}.csv"

    with open('config/terms.json', 'r+', encoding='utf-8') as data_file:
        TERMS_BAG = json.load(data_file)['terms']

    CATEGORIES_COUNT = len(TERMS_BAG) - 2
    COLUMNS_COUNT_1 = CATEGORIES_COUNT + 1
    COLUMNS_COUNT_2 = CATEGORIES_COUNT + 2
    COLUMNS_COUNT_3 = CATEGORIES_COUNT + 3

    with open('config/newspapers.json', 'r+', encoding='utf-8') as data_file:
        NEWSPAPERS = json.load(data_file)

    EPU_DATE_RANGE = {
        'datefrom': get_initial_date(NEWSPAPERS),
        'dateto': get_last_date(NEWSPAPERS)
    }


def get_initial_date(NEWSPAPERS):
    initial_date = date.max
    for key in NEWSPAPERS.keys():
        date_from = NEWSPAPERS[key]['datefrom']
        month_from = int(date_from.split("-")[0])
        year_from = int(date_from.split("-")[1])
        this_date = date(year_from, month_from, 1)
        if this_date < initial_date:
            initial_date = this_date
    return datetime.strftime(initial_date, '%m-%Y')


def get_last_date(NEWSPAPERS):
    last_date = date.min
    for key in NEWSPAPERS.keys():
        date_to = NEWSPAPERS[key]['dateto']
        month_to = int(date_to.split("-")[0])
        year_to = int(date_to.split("-")[1])
        this_date = date(year_to, month_to, 1)
        if this_date > last_date:
            last_date = this_date
    return datetime.strftime(last_date, '%m-%Y')
