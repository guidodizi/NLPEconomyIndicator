import matplotlib.pyplot as plt
import csv

results_path = "results/step3_results_la_republica.csv"
with open(results_path, 'rt', encoding="utf8", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    y_epu_news = []
    x_months = []
    x_ticks = []     
    contador = 0  
    for row in reader:
        y_epu_news.append(float(row['epu_news_std']))
        x_months.append(row['date'])
        x_ticks.append(contador)
        contador += 1

    print ("genero la grafica \n")
    plt.plot(x_months , y_epu_news, 'bo')             
    plt.title('EPU para ' + row['newspaper'])
    plt.axis(["10-2011","10-2014", 0, 0.015])
    plt.show()
