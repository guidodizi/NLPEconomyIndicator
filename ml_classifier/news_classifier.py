# -*- coding: utf-8 -*-
import csv
import json
import re
import sys

import settings
from helper_methods import *


def process_news(newspaper):
    if (newspaper == settings.NEWSPAPERS["el_observador"]["id"]):
        process_el_observador()

    elif (newspaper == settings.NEWSPAPERS["la_diaria"]["id"]):
        process_la_diaria()

    elif (newspaper == settings.NEWSPAPERS["busqueda"]["id"]):
        process_busqueda()


def process_el_observador():
    return 0


def process_la_diaria():
    return 0


def process_busqueda():
    return 0
