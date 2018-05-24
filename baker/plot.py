import matplotlib.pyplot as plt
import csv

with open('results/step2_results_la_republica.csv', 'rt', encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile)
    y_total_news = []
    x_months = []
    x_ticks = []     
    contador = 0  
    for row in reader:
        y_total_news.append(float(row['epu_news_rel']))
        x_months.append(row['date'])  
        x_ticks.append(contador)  
        contador += 1

    print ("genero la grafica \n")
    # y_total_news.sort()
    plt.plot(x_months , y_total_news)             
    plt.title('EPU para ' + row['newspaper'])
    plt.axis(["10-2011","10-2014", 0, 0.015])
    plt.show()