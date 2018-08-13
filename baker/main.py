# -*- coding: utf-8 -*-
import news_processor
import results_processor
import settings
from helper_methods import *


def process_news(newspaper):
    if (newspaper == settings.NEWSPAPERS["la_republica"]["id"]):
        news_processor.process_la_republica()

    elif (newspaper == settings.NEWSPAPERS["el_observador"]["id"]):
        news_processor.process_el_observador()

    elif (newspaper == settings.NEWSPAPERS["la_diaria"]["id"]):
        news_processor.process_la_diaria()

    elif (newspaper == settings.NEWSPAPERS["busqueda"]["id"]):
        news_processor.process_busqueda()


# MAIN
print_presentation()
settings.init()

# Input sections
option = options_input_section()

if (option == "generar_epu"):
    # Generate EPU index from individual newspaper results
    results_processor.generate_epu_index()
else:
    newspaper = option
    print_processing_message(newspaper)

    # Execute news processing (generate raw results)
    process_news(newspaper)

    # Scale results by month articles count
    results_processor.scale_to_relative_count(newspaper)

    # Standardize results to unit standard deviation
    results_processor.scale_to_unit_standard_deviation(newspaper)

print_finish()