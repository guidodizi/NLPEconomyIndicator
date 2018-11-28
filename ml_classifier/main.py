# -*- coding: utf-8 -*-
import classifier_generator
import news_classifier
import results_processor
import settings
from helper_methods import *

# MAIN (Machine Learning classifier method)
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

    # Train the ML algorithms
    # classifier_generator.generate_training_set_tagtog() # TODO: uncomment this method and dinamically generate training set?
    ml_classifier = classifier_generator.text_preproccessing()

    # Execute news classification (generate raw results)
    news_classifier.process_news(newspaper, ml_classifier)

    # Scale results by month articles count
    results_processor.scale_to_relative_count(newspaper)

    # Standardize results to unit standard deviation
    results_processor.scale_to_unit_standard_deviation(newspaper)

print_finish()
