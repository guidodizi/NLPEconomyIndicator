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
    global SMALL_TRAINING_SET_FILEPATH
    global FULL_TRAINING_SET_FILEPATH
    global NEWSPAPERS
    global EPU_DATE_RANGE
    global TAGTOG_PATH
    global CAT0_PATH
    global CAT1_PATH
    global CAT2_PATH
    global TAGTOG_KEY_NAME

    STEP_1_2_3_FILEPATH = "results/ml_step{0}_results_{1}.csv"
    STEP_4_FILEPATH = "results/ml_step4_results_average.csv"
    EPU_INDEX_FILEPATH = "results/ml_epu_index_uruguay.csv"
    NEWS_JSON_FILEPATH = "../news/{0}/{1}/{2}/data.json"
    NEWS_XML_FILEPATH = "../news/{0}/{1}/{2}/{0}.xml"
    NEWS_COUNT_FILEPATH = "../news/{0}/cant_noticias_{0}.csv"
    SMALL_TRAINING_SET_FILEPATH = "training_sets/small_training_news_60.json"
    FULL_TRAINING_SET_FILEPATH = "training_sets/full_training_news.json"

    TAGTOG_PATH = "training_sets/tagtog/"
    CAT0_PATH = "data/0/"
    CAT1_PATH = "data/1/"
    CAT2_PATH = "data/2/"

    TAGTOG_KEY_NAME = "m_3"

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
