# -*- coding: utf-8 -*-
import csv
import json
import os
import sys

import numpy as np
import pandas as pd
import news_preprocessor
import guidedlda
import Stemmer

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV

# Plotting tools
import pyLDAvis
import pyLDAvis.sklearn
import matplotlib.pyplot as plt

import results_file_handler
import settings
import helper_methods



def get_documents_vecotirzed(with_stemming):

    if (with_stemming):
        stemmer = Stemmer.Stemmer('spanish')
        stop_words_spanish = frozenset(stemmer.stemWords(["0","1","2","3","4","5","6","7","8","9","_","a","actualmente","acuerdo","adelante","ademas","además","adrede","afirmó","agregó","ahi","ahora","ahí","al","algo","alguna","algunas","alguno","algunos","algún","alli","allí","alrededor","ambos","ampleamos","antano","antaño","ante","anterior","antes","apenas","aproximadamente","aquel","aquella","aquellas","aquello","aquellos","aqui","aquél","aquélla","aquéllas","aquéllos","aquí","arriba","arribaabajo","aseguró","asi","así","atras","aun","aunque","ayer","añadió","aún","b","bajo","bastante","bien","breve","buen","buena","buenas","bueno","buenos","c","cada","casi","cerca","cierta","ciertas","cierto","ciertos","cinco","claro","comentó","como","con","conmigo","conocer","conseguimos","conseguir","considera","consideró","consigo","consigue","consiguen","consigues","contigo","contra","cosas","creo","cual","cuales","cualquier","cuando","cuanta","cuantas","cuanto","cuantos","cuatro","cuenta","cuál","cuáles","cuándo","cuánta","cuántas","cuánto","cuántos","cómo","d","da","dado","dan","dar","de","debajo","debe","deben","debido","decir","dejó","del","delante","demasiado","demás","dentro","deprisa","desde","despacio","despues","después","detras","detrás","dia","dias","dice","dicen","dicho","dieron","diferente","diferentes","dijeron","dijo","dio","donde","dos","durante","día","días","dónde","e","ejemplo","el","ella","ellas","ello","ellos","embargo","empleais","emplean","emplear","empleas","empleo","en","encima","encuentra","enfrente","enseguida","entonces","entre","era","erais","eramos","eran","eras","eres","es","esa","esas","ese","eso","esos","esta","estaba","estabais","estaban","estabas","estad","estada","estadas","estado","estados","estais","estamos","estan","estando","estar","estaremos","estará","estarán","estarás","estaré","estaréis","estaría","estaríais","estaríamos","estarían","estarías","estas","este","estemos","esto","estos","estoy","estuve","estuviera","estuvierais","estuvieran","estuvieras","estuvieron","estuviese","estuvieseis","estuviesen","estuvieses","estuvimos","estuviste","estuvisteis","estuviéramos","estuviésemos","estuvo","está","estábamos","estáis","están","estás","esté","estéis","estén","estés","ex","excepto","existe","existen","explicó","expresó","f","fin","final","fue","fuera","fuerais","fueran","fueras","fueron","fuese","fueseis","fuesen","fueses","fui","fuimos","fuiste","fuisteis","fuéramos","fuésemos","g","general","gran","grandes","gueno","h","ha","haber","habia","habida","habidas","habido","habidos","habiendo","habla","hablan","habremos","habrá","habrán","habrás","habré","habréis","habría","habríais","habríamos","habrían","habrías","habéis","había","habíais","habíamos","habían","habías","hace","haceis","hacemos","hacen","hacer","hacerlo","haces","hacia","haciendo","hago","han","has","hasta","hay","haya","hayamos","hayan","hayas","hayáis","he","hecho","hemos","hicieron","hizo","horas","hoy","hube","hubiera","hubierais","hubieran","hubieras","hubieron","hubiese","hubieseis","hubiesen","hubieses","hubimos","hubiste","hubisteis","hubiéramos","hubiésemos","hubo","i","igual","incluso","indicó","informo","informó","intenta","intentais","intentamos","intentan","intentar","intentas","intento","ir","j","junto","k","l","la","lado","largo","las","le","lejos","les","llegó","lleva","llevar","lo","los","luego","lugar","m","mal","manera","manifestó","mas","mayor","me","mediante","medio","mejor","mencionó","menos","menudo","mi","mia","mias","mientras","mio","mios","mis","misma","mismas","mismo","mismos","modo","momento","mucha","muchas","mucho","muchos","muy","más","mí","mía","mías","mío","míos","n","nada","nadie","ni","ninguna","ningunas","ninguno","ningunos","ningún","no","nos","nosotras","nosotros","nuestra","nuestras","nuestro","nuestros","nueva","nuevas","nuevo","nuevos","nunca","o","ocho","os","otra","otras","otro","otros","p","pais","para","parece","parte","partir","pasada","pasado","paìs","peor","pero","pesar","poca","pocas","poco","pocos","podeis","podemos","poder","podria","podriais","podriamos","podrian","podrias","podrá","podrán","podría","podrían","poner","por","por qué","porque","posible","primer","primera","primero","primeros","principalmente","pronto","propia","propias","propio","propios","proximo","próximo","próximos","pudo","pueda","puede","pueden","puedo","pues","q","qeu","que","quedó","queremos","quien","quienes","quiere","quiza","quizas","quizá","quizás","quién","quiénes","qué","r","raras","realizado","realizar","realizó","repente","respecto","s","sabe","sabeis","sabemos","saben","saber","sabes","sal","salvo","se","sea","seamos","sean","seas","segun","segunda","segundo","según","seis","ser","sera","seremos","será","serán","serás","seré","seréis","sería","seríais","seríamos","serían","serías","seáis","señaló","si","sido","siempre","siendo","siete","sigue","siguiente","sin","sino","sobre","sois","sola","solamente","solas","solo","solos","somos","son","soy","soyos","su","supuesto","sus","suya","suyas","suyo","suyos","sé","sí","sólo","t","tal","tambien","también","tampoco","tan","tanto","tarde","te","temprano","tendremos","tendrá","tendrán","tendrás","tendré","tendréis","tendría","tendríais","tendríamos","tendrían","tendrías","tened","teneis","tenemos","tener","tenga","tengamos","tengan","tengas","tengo","tengáis","tenida","tenidas","tenido","tenidos","teniendo","tenéis","tenía","teníais","teníamos","tenían","tenías","tercera","ti","tiempo","tiene","tienen","tienes","toda","todas","todavia","todavía","todo","todos","total","trabaja","trabajais","trabajamos","trabajan","trabajar","trabajas","trabajo","tras","trata","través","tres","tu","tus","tuve","tuviera","tuvierais","tuvieran","tuvieras","tuvieron","tuviese","tuvieseis","tuviesen","tuvieses","tuvimos","tuviste","tuvisteis","tuviéramos","tuviésemos","tuvo","tuya","tuyas","tuyo","tuyos","tú","u","ultimo","un","una","unas","uno","unos","usa","usais","usamos","usan","usar","usas","uso","usted","ustedes","v","va","vais","valor","vamos","van","varias","varios","vaya","veces","ver","verdad","verdadera","verdadero","vez","vosotras","vosotros","voy","vuestra","vuestras","vuestro","vuestros","w","x","y","ya","yo","z","él","éramos","ésa","ésas","ése","ésos","ésta","éstas","éste","éstos","última","últimas","último","últimos"
                                    "td","tr","com","width","img","class","height","src","table","gif","hspace","tbody","border", "style", 
                                    "right", "style","margin","ltr","blockquote","qu"]))
    else:
        stop_words_spanish = frozenset(["0","1","2","3","4","5","6","7","8","9","_","a","actualmente","acuerdo","adelante","ademas","además","adrede","afirmó","agregó","ahi","ahora","ahí","al","algo","alguna","algunas","alguno","algunos","algún","alli","allí","alrededor","ambos","ampleamos","antano","antaño","ante","anterior","antes","apenas","aproximadamente","aquel","aquella","aquellas","aquello","aquellos","aqui","aquél","aquélla","aquéllas","aquéllos","aquí","arriba","arribaabajo","aseguró","asi","así","atras","aun","aunque","ayer","añadió","aún","b","bajo","bastante","bien","breve","buen","buena","buenas","bueno","buenos","c","cada","casi","cerca","cierta","ciertas","cierto","ciertos","cinco","claro","comentó","como","con","conmigo","conocer","conseguimos","conseguir","considera","consideró","consigo","consigue","consiguen","consigues","contigo","contra","cosas","creo","cual","cuales","cualquier","cuando","cuanta","cuantas","cuanto","cuantos","cuatro","cuenta","cuál","cuáles","cuándo","cuánta","cuántas","cuánto","cuántos","cómo","d","da","dado","dan","dar","de","debajo","debe","deben","debido","decir","dejó","del","delante","demasiado","demás","dentro","deprisa","desde","despacio","despues","después","detras","detrás","dia","dias","dice","dicen","dicho","dieron","diferente","diferentes","dijeron","dijo","dio","donde","dos","durante","día","días","dónde","e","ejemplo","el","ella","ellas","ello","ellos","embargo","empleais","emplean","emplear","empleas","empleo","en","encima","encuentra","enfrente","enseguida","entonces","entre","era","erais","eramos","eran","eras","eres","es","esa","esas","ese","eso","esos","esta","estaba","estabais","estaban","estabas","estad","estada","estadas","estado","estados","estais","estamos","estan","estando","estar","estaremos","estará","estarán","estarás","estaré","estaréis","estaría","estaríais","estaríamos","estarían","estarías","estas","este","estemos","esto","estos","estoy","estuve","estuviera","estuvierais","estuvieran","estuvieras","estuvieron","estuviese","estuvieseis","estuviesen","estuvieses","estuvimos","estuviste","estuvisteis","estuviéramos","estuviésemos","estuvo","está","estábamos","estáis","están","estás","esté","estéis","estén","estés","ex","excepto","existe","existen","explicó","expresó","f","fin","final","fue","fuera","fuerais","fueran","fueras","fueron","fuese","fueseis","fuesen","fueses","fui","fuimos","fuiste","fuisteis","fuéramos","fuésemos","g","general","gran","grandes","gueno","h","ha","haber","habia","habida","habidas","habido","habidos","habiendo","habla","hablan","habremos","habrá","habrán","habrás","habré","habréis","habría","habríais","habríamos","habrían","habrías","habéis","había","habíais","habíamos","habían","habías","hace","haceis","hacemos","hacen","hacer","hacerlo","haces","hacia","haciendo","hago","han","has","hasta","hay","haya","hayamos","hayan","hayas","hayáis","he","hecho","hemos","hicieron","hizo","horas","hoy","hube","hubiera","hubierais","hubieran","hubieras","hubieron","hubiese","hubieseis","hubiesen","hubieses","hubimos","hubiste","hubisteis","hubiéramos","hubiésemos","hubo","i","igual","incluso","indicó","informo","informó","intenta","intentais","intentamos","intentan","intentar","intentas","intento","ir","j","junto","k","l","la","lado","largo","las","le","lejos","les","llegó","lleva","llevar","lo","los","luego","lugar","m","mal","manera","manifestó","mas","mayor","me","mediante","medio","mejor","mencionó","menos","menudo","mi","mia","mias","mientras","mio","mios","mis","misma","mismas","mismo","mismos","modo","momento","mucha","muchas","mucho","muchos","muy","más","mí","mía","mías","mío","míos","n","nada","nadie","ni","ninguna","ningunas","ninguno","ningunos","ningún","no","nos","nosotras","nosotros","nuestra","nuestras","nuestro","nuestros","nueva","nuevas","nuevo","nuevos","nunca","o","ocho","os","otra","otras","otro","otros","p","pais","para","parece","parte","partir","pasada","pasado","paìs","peor","pero","pesar","poca","pocas","poco","pocos","podeis","podemos","poder","podria","podriais","podriamos","podrian","podrias","podrá","podrán","podría","podrían","poner","por","por qué","porque","posible","primer","primera","primero","primeros","principalmente","pronto","propia","propias","propio","propios","proximo","próximo","próximos","pudo","pueda","puede","pueden","puedo","pues","q","qeu","que","quedó","queremos","quien","quienes","quiere","quiza","quizas","quizá","quizás","quién","quiénes","qué","r","raras","realizado","realizar","realizó","repente","respecto","s","sabe","sabeis","sabemos","saben","saber","sabes","sal","salvo","se","sea","seamos","sean","seas","segun","segunda","segundo","según","seis","ser","sera","seremos","será","serán","serás","seré","seréis","sería","seríais","seríamos","serían","serías","seáis","señaló","si","sido","siempre","siendo","siete","sigue","siguiente","sin","sino","sobre","sois","sola","solamente","solas","solo","solos","somos","son","soy","soyos","su","supuesto","sus","suya","suyas","suyo","suyos","sé","sí","sólo","t","tal","tambien","también","tampoco","tan","tanto","tarde","te","temprano","tendremos","tendrá","tendrán","tendrás","tendré","tendréis","tendría","tendríais","tendríamos","tendrían","tendrías","tened","teneis","tenemos","tener","tenga","tengamos","tengan","tengas","tengo","tengáis","tenida","tenidas","tenido","tenidos","teniendo","tenéis","tenía","teníais","teníamos","tenían","tenías","tercera","ti","tiempo","tiene","tienen","tienes","toda","todas","todavia","todavía","todo","todos","total","trabaja","trabajais","trabajamos","trabajan","trabajar","trabajas","trabajo","tras","trata","través","tres","tu","tus","tuve","tuviera","tuvierais","tuvieran","tuvieras","tuvieron","tuviese","tuvieseis","tuviesen","tuvieses","tuvimos","tuviste","tuvisteis","tuviéramos","tuviésemos","tuvo","tuya","tuyas","tuyo","tuyos","tú","u","ultimo","un","una","unas","uno","unos","usa","usais","usamos","usan","usar","usas","uso","usted","ustedes","v","va","vais","valor","vamos","van","varias","varios","vaya","veces","ver","verdad","verdadera","verdadero","vez","vosotras","vosotros","voy","vuestra","vuestras","vuestro","vuestros","w","x","y","ya","yo","z","él","éramos","ésa","ésas","ése","ésos","ésta","éstas","éste","éstos","última","últimas","último","últimos"
                                    "td","tr","com","width","img","class","height","src","table","gif","hspace","tbody","border", "style", 
                                    "right", "style","margin","ltr","blockquote","qu"])
    
    documents, documents_date = news_preprocessor.generate_array_with_news(with_stemming)
    
    no_features = 1000
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features= no_features, stop_words=stop_words_spanish)
    tf = tf_vectorizer.fit_transform(documents)    

    print ("Documentos preprocesados")
    return documents, documents_date, tf, tf_vectorizer

def lda_algorithm(tf):
    
    # LDA can only use raw term counts for LDA because it is a probabilistic graphical model        
    lda_algorithm = LatentDirichletAllocation(n_components=settings.NO_TOPICS, max_iter=5, learning_method='online', learning_offset=50.,random_state=0)
    lda = lda_algorithm.fit(tf)  
    return lda_algorithm, lda  

def guided_lda(tf, with_stemming):

    # X = guidedlda.datasets.load_data(guidedlda.datasets.NYT)
    # vocab = guidedlda.datasets.load_vocab(guidedlda.datasets.NYT)
    # word2id = dict((v, idx) for idx, v in enumerate(tf_feature_names))

    if (with_stemming):
        stemmer = Stemmer.Stemmer('spanish')
        
        seed_topic_list = [stemmer.stemWords(["impuestos","impuesto","impositivo"]),
                        stemmer.stemWords(["gasto gubernamental","gasto del gobierno"]),
                        stemmer.stemWords(["ajuste fiscal","política fiscal"]),
                        stemmer.stemWords(["reserva federal", "oferta monetaria"]),
                        stemmer.stemWords(["deuda soberana","crisis monetaria","colapso de moneda"]),
                        stemmer.stemWords(["programas de gobierno","seguridad social","bienestar"]),
                        stemmer.stemWords(["tarifas de importación","impuestos de importación"]),
                        stemmer.stemWords(["gobierno","autoridades","parlamento"])                                 
                        ]
    else:
        seed_topic_list = [["impuestos","impuesto","impositivo"],
                        ["gasto gubernamental","gasto del gobierno"],
                        ["ajuste fiscal","política fiscal"],
                        ["reserva federal", "oferta monetaria"],
                        ["deuda soberana","crisis monetaria","colapso de moneda"],
                        ["programas de gobierno","seguridad social","bienestar"],
                        ["tarifas de importación","impuestos de importación"],
                        ["gobierno","autoridades","parlamento"]                                 
                        ]

    guided_lda_algorithm = guidedlda.GuidedLDA(n_topics=9, n_iter=100, random_state=7, refresh=20)

    print ("guidedLda algorithm")
    seed_topics = {}
    index_id = 0
    for t_id, st in enumerate(seed_topic_list):
        for word in st:
            seed_topics[index_id] = t_id
            index_id += 1
        index_id += 1
        
    guided_lda = guided_lda_algorithm.fit(tf, seed_topics=seed_topics, seed_confidence=1)    
    print ("guidedLda fit")    
    return guided_lda_algorithm, guided_lda

def get_and_print_results(tf, tf_vectorizer, algorithm,fit_algorithm, documents_date):
    # En esta variable esta cada uno de los documentos con un arreglo de los 30 topicos y que valor tiene para cada 1
    documents_categorized_with_topics = algorithm.transform(tf)
    quantity_list = helper_methods.create_quantity_list()

    # contar cantidad de veces que apaparece cada topico
    index = 0
    for doc_cat in documents_categorized_with_topics:        
        topic = np.where(doc_cat == doc_cat.max())[0][0]
        month = int(documents_date[index].split('/')[0])
        year = int(documents_date[index].split('/')[1])
        # se puede mejorar perfomance 
        for obj in quantity_list:
            if obj.Month == month and obj.Year == year:
                obj.Topics[topic] += 1
                break    
        index += 1

    no_top_words = 10
    
    topic_words = helper_methods.display_topics(fit_algorithm, tf_vectorizer.get_feature_names(), no_top_words)         

    helper_methods.write_csv_file_step1(quantity_list)

    helper_methods.scale_to_unit_standard_deviation()

    helper_methods.scale_to_100_mean()
    
    return topic_words, documents_categorized_with_topics

def print_documents_with_topics(documents, documents_with_topics, topic_words):
    
    data = []
    index = 0
    topics_showed = []
    first = True       
    for doc in documents_with_topics:
        if len(topics_showed) == settings.NO_TOPICS:
            break
        topic_index = np.where(doc == doc.max())[0][0] 
        if topic_index == 6 and first:
            first = False
        else:
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