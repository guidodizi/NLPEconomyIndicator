# -*- coding: utf-8 -*-
import results_processor
import news_processor
from helper_methods import *

def process_news(newspaper):
    print_processing_message(newspaper)
    if (newspaper == "la_republica"):
        news_processor.process_la_republica()
    elif (newspaper == "el_observador"):
        news_processor.process_el_observador()
    elif (newspaper == "la_diaria"):
        news_processor.process_la_diaria()
    elif (newspaper == "busqueda"):
        news_processor.process_busqueda()

# MAIN
print_presentation()

# Input sections
option = options_input_section()

if (option == "generar_epu"):
    # Generate EPU index from individual newspaper results
    results_processor.generate_epu_index()
else:
    newspaper = option

    # Execute news processing (generate raw results)
    process_news(newspaper)

    # Scale results by month articles count
    results_processor.scale_to_relative_count(newspaper)

    # Standardize results to unit standard deviation
    results_processor.scale_to_unit_standard_deviation(newspaper)

print_finish()
