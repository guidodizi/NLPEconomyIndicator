# -*- coding: utf-8 -*-
import news_processor
import results_processor
import settings
import time
from helper_methods import *

# MAIN (Baker method)
print_presentation()
settings.init()

# Input sections
option = options_input_section()

if (option == "generar_epu"):
    # Generate EPU index from individual newspaper results
    start_time = time.time()
    results_processor.generate_epu_index()
else:
    start_time = time.time()
    newspaper = option
    print_processing_message(newspaper)

    # Execute news processing (generate raw results)
    news_processor.process_news(newspaper)

    # Scale results by month articles count
    results_processor.scale_to_relative_count(newspaper)

    # Standardize results to unit standard deviation
    results_processor.scale_to_unit_standard_deviation(newspaper)

print_finish()
print("\n--- Tiempo de ejecución: %s segundos --- \n" % (round(time.time() - start_time, 1)))
