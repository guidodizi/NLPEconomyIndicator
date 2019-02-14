# -*- coding: utf-8 -*-
import json
from datetime import date
from datetime import datetime

# FOR GLOBAL VARIABLES AND DATA


def init():
    global NEWSPAPERS    
    global NEWS_JSON_FILEPATH
    
    NEWS_JSON_FILEPATH = "../news/{0}/{1}/{2}/data.json"
    with open('config/newspapers.json', 'r+', encoding='utf-8') as data_file:
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
