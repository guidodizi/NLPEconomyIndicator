# -*- coding: utf-8 -*-
import settings
import news_preprocessor
import helper_methods
import results_processor
import quantity_date

option, with_stemming = helper_methods.options_input_section()

# MAIN (LDA method)
settings.init()

#obtengo los documentos
documents, documents_date, documents_vectorized, tf_vectorizer, obs_documents, obs_documents_date, obs_documents_vectorized = results_processor.get_documents_vecotirzed(with_stemming)

if (option == "bestk"):
    #################### ALGOTIMO ARTICULO QUE HACE TODO########################
    results_processor.grid_search_best_components(documents_vectorized, documents, tf_vectorizer)
else:
    if (option == "lda"):
        algorithm, fit_algorithm = results_processor.lda_algorithm(documents_vectorized)        
        
    elif (option == "guidedlda"):
        algorithm, fit_algorithm = results_processor.guided_lda(documents_vectorized,tf_vectorizer, with_stemming)
    
    topic_words, documents_categorized_with_topics = results_processor.get_and_print_results(documents_vectorized, tf_vectorizer, algorithm,fit_algorithm, documents_date)
    
    #################### ALGORITMO PARA IMPRIMIR UN DOCUMENTO DE CADA TOPICO
    results_processor.print_documents_with_topics(documents, documents_categorized_with_topics, topic_words)

