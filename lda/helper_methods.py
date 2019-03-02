# -*- coding: utf-8 -*-
import json
import sys
import quantity_date
import csv
import numpy as np
import pandas as pd

from datetime import datetime
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV

# Plotting tools
import pyLDAvis
import pyLDAvis.sklearn
import matplotlib.pyplot as plt

import results_file_handler
import settings

# HELPER METHODS
# ----- Auxiliar -----

def month_year_iter(date_from, date_to):
    start_month = int(date_from.split("-")[0])
    start_year = int(date_from.split("-")[1])
    end_month = int(date_to.split("-")[0])
    end_year = int(date_to.split("-")[1])
    ym_start = 12 * start_year + start_month - 1
    ym_end = 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m+1


def display_topics(model, feature_names, no_top_words):
    f= open("terms.txt","w+")
    topic_words = []
    for topic_idx, topic in enumerate(model.components_):
        words = " ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]])
        print ("Topic %d:" % (topic_idx))
        print (words)
        f.write("Topic %d:" % (topic_idx))
        f.write(words)        
        f.write("\n")
        topic_words.append(words)
    
    return topic_words


def create_quantity_list():
    quantity_list = []
    date_from = settings.FULL_DATE['datefrom']
    date_to = settings.FULL_DATE['dateto']
    date_iter = month_year_iter(date_from, date_to)

    for date in date_iter: 
        year, month = date[0], date[1]
        date = quantity_date.Quantity_Date(month, year, settings.NO_TOPICS)  
        quantity_list.append(date)
    return quantity_list            


def write_csv_file_step1(quantiy_list):
    filepath = settings.STEP2_FILEPATH
    base_data = ["date", "epu_index"]

    for i in range(0,settings.NO_TOPICS):        
        base_data.append("Tema " + str(i))

    with open(filepath, 'w', encoding='utf-8', newline='') as data_file:
        wr = csv.writer(data_file, quoting=csv.QUOTE_NONNUMERIC)        
        wr.writerow(base_data)        
        for item in quantiy_list:
            row_data = [str(item.Month)+ '-' + str(item.Year), sum(item.Topics)]
            row_data = row_data + item.Topics
            wr.writerow(row_data)


#STEP 2
#TODO dividir entre la cantidad de noticias por mes
#STEP 3 
def scale_to_unit_standard_deviation():
    previous_results_path = settings.STEP2_FILEPATH
    filepath = settings.STEP3_FILEPATH
    results_file_handler.create_step3_results_file()

    step2_matrix = np.loadtxt(open(previous_results_path, "rb"),
                              delimiter=",", usecols=range(1, settings.NO_TOPICS + 2), skiprows=1)

    std_dev_dict = {}
    for i in range(len(step2_matrix[0])):
        step2_index = step2_matrix[:, i]
        std_dev = np.std(step2_index, dtype=np.float64)
        std_dev_dict[i] = std_dev

    with open(previous_results_path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        next(csvreader)  # Skips headers row                
        for row in csvreader:
            cols = len(row)
            date = row[0]

            col_data = [date]
            for i in range(1, cols):
                col_data.append(row[i]/std_dev_dict[i-1])  

            results_file_handler.append_csv_file_row(filepath, col_data)


#STEP 4
def scale_to_100_mean():
    previous_results_path = settings.STEP3_FILEPATH
    filepath = settings.RESULT_FILEPATH
    results_file_handler.create_epu_index_file()

    step4_matrix = np.loadtxt(open(previous_results_path, "rb"),
                              delimiter=",", usecols=range(1,settings.NO_TOPICS + 2), skiprows=1)    

    mean_coef_dict = {}
    for i in range(len(step4_matrix[0])):
        step4_index = step4_matrix[:, i]
        mean = np.mean(step4_index, dtype=np.float64)
        coef = (100 / mean)
        mean_coef_dict[i] = coef

    with open(previous_results_path, 'r+', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        next(csvreader)  # Skips headers row
        for row in csvreader:
            date = row[0]
            data = [date]

            for i in range(1, settings.NO_TOPICS):
                data.append(row[i]*mean_coef_dict[i-1])

            results_file_handler.append_csv_file_row(filepath, data)


def print_documents_with_topics(documents, documents_with_topics, topic_words):
    
    data = []
    index = 0
    topics_showed = []
    for doc in documents_with_topics:
        if len(topics_showed) == settings.NO_TOPICS:
            break
        topic_index = np.where(doc == doc.max())[0][0]      
        if topic_index not in topics_showed:  
            topics_showed.append(topic_index)
            data.append({"noticia": documents[index], "palabras_tema": topic_words[topic_index], 'tema': str(topic_index)})
        index += 1
    
    with open(settings.DOCUMENTS_FILEPATH, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def get_best_number_of_topic(tf_documents):

    prob_for_no_topic = []    
    for no_topics in range(8,40):
        
        lda_algorithm = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0)
        lda_algorithm.fit(tf_documents)
        documents_categorized_with_topics = lda_algorithm.transform(tf_documents)
        sum_prob = 0

        for doc in documents_categorized_with_topics:
            doc_prob = max(doc)
            sum_prob += doc_prob

        sum_prob = sum_prob / len(documents_categorized_with_topics)
        prob_for_no_topic.append({"no_topics": no_topics, "prob":sum_prob})
        print (no_topics)

    with open(settings.NO_TOPICS_FILEPATH, 'w', encoding='utf-8') as outfile:
        json.dump(prob_for_no_topic, outfile, ensure_ascii=False)

    
def grid_search_best_components(data_vectorized, documents, tf_vectorizer):
    # Define Search Param
    
    #search_params = {'n_components': [6,7,8,9,10,11,12,15,20,25,30] , 'learning_decay': [.9]}
    search_params = {'n_components': [9], 'learning_decay': [.9]}

    # Init the Model
    lda = LatentDirichletAllocation()

    # Init Grid Search Class
    model = GridSearchCV(lda, param_grid=search_params)

    # Do the Grid Search
    model.fit(data_vectorized)

    # Best Model
    best_lda_model = model.best_estimator_

    # Model Parameters
    print("Best Model's Params: ", model.best_params_)

    # Log Likelihood Score
    print("Best Log Likelihood Score: ", model.best_score_)

    # Perplexity
    print("Model Perplexity: ", best_lda_model.perplexity(data_vectorized))


    # # Get Log Likelyhoods from Grid Search Output
    # n_topics = [6,7,8,9,10,11,12,15,20,25,30]    
    ### NO EXISTE EL grid_scores_
    # log_likelyhoods_7 = [round(gscore.mean_validation_score) for gscore in model.grid_scores_ if gscore.parameters['learning_decay']==0.7]
    # log_likelyhoods_9 = [round(gscore.mean_validation_score) for gscore in model.grid_scores_ if gscore.parameters['learning_decay']==0.9]

    # # Show graph
    # plt.figure(figsize=(12, 8))    
    # plt.plot(n_topics, log_likelyhoods_7, label='0.7')
    # plt.plot(n_topics, log_likelyhoods_9, label='0.9')
    # plt.title("Choosing Optimal LDA Model")
    # plt.xlabel("Num Topics")
    # plt.ylabel("Log Likelyhood Scores")
    # plt.legend(title='Learning decay', loc='best')
    # plt.show()

    # Create Document - Topic Matrix
    lda_output = best_lda_model.transform(data_vectorized)

    # column names
    #### best_lda_model.n_topics me da nulo y explota
    # topicnames = ["Topic" + str(i) for i in range(best_lda_model.n_topics)]
    topicnames = ["Topic" + str(i) for i in range(9)]

    # index names
    docnames = ["Doc" + str(i) for i in range(len(documents))]

    # Make the pandas dataframe
    df_document_topic = pd.DataFrame(np.round(lda_output, 2), columns=topicnames, index=docnames)

    # Get dominant topic for each document
    dominant_topic = np.argmax(df_document_topic.values, axis=1)
    df_document_topic['dominant_topic'] = dominant_topic

    # Styling
    def color_green(val):
        color = 'green' if val > .1 else 'black'
        return 'color: {col}'.format(col=color)

    def make_bold(val):
        weight = 700 if val > .1 else 400
        return 'font-weight: {weight}'.format(weight=weight)

    # Apply Style
    df_document_topics = df_document_topic.head(15).style.applymap(color_green).applymap(make_bold)
    # falta ver como imprimir df_document_topics 
    df_document_topics

    df_topic_distribution = df_document_topic['dominant_topic'].value_counts().reset_index(name="Num Documents")
    df_topic_distribution.columns = ['Topic Num', 'Num Documents']
    # falta ver como imprimir df_topic_distribution 
    df_topic_distribution   

    ## explota dice que necesita IPython
    pyLDAvis.enable_notebook()
    panel = pyLDAvis.sklearn.prepare(best_lda_model, data_vectorized, tf_vectorizer, mds='tsne')
    panel