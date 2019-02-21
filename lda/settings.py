# -*- coding: utf-8 -*-
import json
from datetime import date
from datetime import datetime

# FOR GLOBAL VARIABLES AND DATA


def init():
    global NEWSPAPERS    
    global TERMS_BAG
    global NEWS_JSON_FILEPATH
    global FULL_DATE    
    global STEP1_FILEPATH
    global STEP2_FILEPATH
    global STEP3_FILEPATH    
    global RESULT_FILEPATH
    global NO_TOPICS

    NO_TOPICS = 30

    STEP1_FILEPATH = "C:/NLP/NLPEconomyIndicator/lda/results/lda_step1.csv"
    STEP2_FILEPATH = "C:/NLP/NLPEconomyIndicator/lda/results/lda_step2.csv"
    STEP3_FILEPATH = "C:/NLP/NLPEconomyIndicator/lda/results/lda_step3.csv"    
    RESULT_FILEPATH = "C:/NLP/NLPEconomyIndicator/lda/results/lda_epu.csv"
    
    with open('C:/NLP/NLPEconomyIndicator/lda/config/full_date.json', 'r+', encoding='utf-8') as data_file:
        FULL_DATE = json.load(data_file)

    with open('C:/NLP/NLPEconomyIndicator/lda/config/terms.json', 'r+', encoding='utf-8') as data_file:
        TERMS_BAG = json.load(data_file)['terms']

    NEWS_JSON_FILEPATH = "C:/NLP/NLPEconomyIndicator/news/{0}/{1}/{2}/data.json"
    with open('C:/NLP/NLPEconomyIndicator/lda/config/newspapers.json', 'r+', encoding='utf-8') as data_file:
        NEWSPAPERS = json.load(data_file)


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
