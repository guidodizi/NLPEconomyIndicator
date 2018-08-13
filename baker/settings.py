# -*- coding: utf-8 -*-
import json

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

    with open('config/newspapers.json', 'r+', encoding='utf-8') as data_file:
        NEWSPAPERS = json.load(data_file)

    # TODO: hacer que lo calcule a partir de la config en NEWSPAPERS
    EPU_DATE_RANGE = {
        'datefrom': '01-2002',
        'dateto': '05-2018'
    }
