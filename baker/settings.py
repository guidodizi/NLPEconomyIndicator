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
    global NEWS_ECONOMY_JSON_FILEPATH
    global NEWS_ECONOMY_DIRECTORY
    global NEWS_EU_JSON_FILEPATH
    global NEWS_EU_DIRECTORY
    global NEWS_NON_ECONOMY_JSON_FILEPATH
    global NEWS_NON_ECONOMY_DIRECTORY
    global NEWS_XML_FILEPATH
    global NEWS_COUNT_FILEPATH
    global TERMS_BAG
    global NEWSPAPERS
    global CATEGORIES_COUNT
    global COLUMNS_COUNT_1
    global COLUMNS_COUNT_2
    global COLUMNS_COUNT_3
    global EPU_DATE_RANGE
    global WRITE_PROCESSED_NEWS
    global PROCESS_FROM_EU_NEWS_ONLY

    WRITE_PROCESSED_NEWS = False # This writes classified news into "/news/_non_economy/", "/news/_economy/" and "/news/_eu/" directories.
    PROCESS_FROM_EU_NEWS_ONLY = False # Makes processing faster. This can be set to True when the "/news/_eu/" directory exists and has news.

    STEP_1_2_3_FILEPATH = "results/step{0}_results_{1}.csv"
    STEP_4_FILEPATH = "results/step4_results_average.csv"
    EPU_INDEX_FILEPATH = "results/epu_index_uruguay.csv"

    if PROCESS_FROM_EU_NEWS_ONLY:
        WRITE_PROCESSED_NEWS = False # It should not write news to "/news/_eu/" directory.
        NEWS_JSON_FILEPATH = "../news/_eu/{0}/{1}/{2}/data.json"
    else:
        NEWS_JSON_FILEPATH = "../news/{0}/{1}/{2}/data.json"

    NEWS_ECONOMY_JSON_FILEPATH = "../news/_economy/{0}/{1}/{2}/data.json"
    NEWS_ECONOMY_DIRECTORY = "../news/_economy/{0}"
    NEWS_EU_JSON_FILEPATH = "../news/_eu/{0}/{1}/{2}/data.json"
    NEWS_EU_DIRECTORY = "../news/_eu/{0}"
    NEWS_NON_ECONOMY_JSON_FILEPATH = "../news/_non_economy/{0}/{1}/{2}/data.json"
    NEWS_NON_ECONOMY_DIRECTORY = "../news/_non_economy/{0}"
    NEWS_XML_FILEPATH = "../news/{0}/{1}/{2}/{0}.xml"
    NEWS_COUNT_FILEPATH = "../news/{0}/cant_noticias_{0}.csv"

    with open('config/terms.json', 'r+', encoding='utf-8') as data_file:
        TERMS_BAG = json.load(data_file)['terms']

    CATEGORIES_COUNT = len(TERMS_BAG) - 2
    COLUMNS_COUNT_1 = CATEGORIES_COUNT + 1
    COLUMNS_COUNT_2 = CATEGORIES_COUNT + 2
    COLUMNS_COUNT_3 = CATEGORIES_COUNT + 4

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
