# -*- coding: utf-8 -*-
import json
import os
from datetime import date
from random import randint

# This script will generate the news files to upload to TagTog to be annotated.
# It generates one .txt file per news.

# It takes:
# - 520 news from El Observador (from 01/2002 to 09/2018 - 201 months)
# - 280 news from La Diaria (from 08/2009 to 09/2018 - 110 months)
# - 200 news from Búsqueda (from 04/2012 to 09/2018 - 78 months)

# Also it balances the amount of news of each category within Baker's classification:
# - 1/3 of non economy news
# - 1/3 of economy news
# - 1/3 of economic uncertainty (eu) news


NEWS_BY_CATEGORY_FILEPATH = "../news/{0}/{1}/{2}/{3}/data.json"
NEWS_TAGTOG_FILEPATH = "../news/_tagtog/news_{0}.txt"
NEWS_COUNT = 0


def print_presentation():
    print(u"\n---------------------------------------------------------------")
    print(u"---------------------------------------------------------------")
    print(u"Generando base de noticias para TagTog\n")


def print_finish():
    print(u"\nSe generaron los archivos para subir a TagTog.")
    print(u"Se encuentran en la carpeta '/news/_tagtog/'")
    print(u"---------------------------------------------------------------")
    print(u"---------------------------------------------------------------\n")


def format_news_content(original_content):
    news_content = " ".join(original_content.split()) # removes multiple spaces, tabs, and new lines
    news_content = news_content.replace("<strong>", " ")
    news_content = news_content.replace("</strong>", " ")
    news_content = news_content.replace("<br>", " ")
    news_content = news_content.replace("<b>", " ")
    news_content = news_content.replace("</b>", " ")
    news_content = news_content.replace("<p>", " ")
    news_content = news_content.replace("</p>", " ")
    news_content = news_content.replace("<em>", " ")
    news_content = news_content.replace("</em>", " ")
    news_content = news_content.replace("<span>", " ")
    news_content = news_content.replace("</span>", " ")
    news_content = news_content.replace("<i>", " ")
    news_content = news_content.replace("</i>", " ")
    news_content = news_content.replace("<a>", " ")
    news_content = news_content.replace("</a>", " ")
    news_content = news_content.replace("<ul>", " ")
    news_content = news_content.replace("</ul>", " ")
    news_content = news_content.replace("<ol>", " ")
    news_content = news_content.replace("</ol>", " ")
    news_content = news_content.replace("<li>", " ")
    news_content = news_content.replace("</li>", " ")
    news_content = news_content.replace("<!--", " ")
    news_content = news_content.replace("-->", " ")
    news_content = news_content.replace('<font size="1">', " ")
    news_content = news_content.replace('<font size="2">', " ")
    news_content = news_content.replace('<font size="3">', " ")
    news_content = news_content.replace('<font size="4">', " ")
    news_content = news_content.replace('<font size="5">', " ")
    news_content = news_content.replace('<font size="6">', " ")
    news_content = news_content.replace("</font>", " ")
    news_content = news_content.replace('<blockquote dir="ltr" style="MARGIN-RIGHT:" 0px="">', " ")
    news_content = news_content.replace("</blockquote>", " ")
    news_content = news_content.replace('<p align="right">', " ")
    news_content = news_content.replace("<br="">", " ")
    news_content = news_content.replace("&lt;", " ")
    news_content = news_content.replace("&gt;", " ")
    news_content = news_content.replace('<span style="font-size: small;">', " ")
    news_content = news_content.replace('<a href="mailto:eduardoespina2003@yahoo.com" target="blank">', " ")
    news_content = news_content.replace('<a href="mailto:cromanoff@observador.com.uy" target="blank">', " ")
    news_content = news_content.replace('<a href="http://www.dannyfirst.com" target="blank">" target="blank">', " ")
    news_content = news_content.replace('<a href="http://www.ccj.edu.uy" target="blank">', " ")
    news_content = news_content.replace('<strong style="font-size: small;">', " ")
    news_content = news_content.replace('<span style="font-size: large;">', " ")
    news_content = news_content.replace('<span style="font-size: large;">', " ")
    news_content = news_content.replace('<img src="https://www.elobservadormas.com.uy/html/img/frontend/cristianismo.png" alt="">', " ")
    news_content = news_content.replace('<a href="http://www.razonesypersonas.com/">', " ")
    news_content = news_content.replace('<a href="http://www.comfyland.com " target="blank">', " ")
    news_content = news_content.replace('<a href="mailto:pfischer@primerospasosonline.com" target="blank">', " ")
    news_content = news_content.replace('<a href="http://www.descubriendo.org " target="blank">', " ")
    news_content = news_content.replace('<a class="footnote-ref" href="#fn:1" rel="footnote">', " ")
    news_content = news_content.replace('<a class="footnote-ref" href="#fn:2" rel="footnote">', " ")
    news_content = news_content.replace('<a class="footnote-ref" href="#fn:3" rel="footnote">', " ")
    news_content = news_content.replace('<a class="footnote-ref" href="#fn:4" rel="footnote">', " ")
    news_content = news_content.replace('<sup id="fnref:1">', " ")
    news_content = news_content.replace('<sup id="fnref:2">', " ")
    news_content = news_content.replace('<sup id="fnref:3">', " ")
    news_content = news_content.replace('<sup id="fnref:4">', " ")
    news_content = news_content.replace('</sup>', " ")
    news_content = news_content.replace("(AFP)", " ")
    # TODO: remove every HTML tag and any other thing not part from the text
    news_content = " ".join(news_content.split()) # removes multiple spaces, tabs, and new lines (again)
    return news_content


def get_monthly_news_array(category, newspaper, year, month):
    month_news_array = []
    month_news_path = NEWS_BY_CATEGORY_FILEPATH.format(category, newspaper, str(year), str(month))
    if os.path.isfile(month_news_path): # File exists
        with open(month_news_path, encoding='utf-8') as feedsjson:
            month_news_array = json.load(feedsjson)
    return month_news_array


def create_news_file(month_news_array, index):
    global NEWS_COUNT
    NEWS_COUNT = NEWS_COUNT + 1
    count = str(NEWS_COUNT).zfill(4)
    news_filepath = NEWS_TAGTOG_FILEPATH.format(count)
    news_content = format_news_content(month_news_array[index]['doc']['articulo'])

    f = open(news_filepath, 'w', encoding='utf-8')
    f.write(news_content)
    f.close()
    print(u"Archivo 'news_"+count+".txt' generado.")


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


def process_el_observador():
    newspaper = "el_observador"
    date_from = "01-2002"
    date_to = "10-2018"
    process_newspaper(newspaper, date_from, date_to)
    print(u"\nSe terminó de procesar El Observador.\n")


def process_la_diaria():
    newspaper = "la_diaria"
    date_from = "08-2009"
    date_to = "08-2018"
    process_newspaper(newspaper, date_from, date_to)
    print(u"\nSe terminó de procesar La Diaria.\n")


def process_busqueda():
    newspaper = "busqueda"
    date_from = "04-2012"
    date_to = "08-2018"
    process_newspaper(newspaper, date_from, date_to)
    print(u"\nSe terminó de procesar Búsqueda.\n")


def process_newspaper(newspaper, date_from, date_to):
    date_iter = month_year_iter(date_from, date_to)
    for date in date_iter:
        year, month = date[0], date[1]
        for category in ["_non_economy", "_economy", "_eu"]:
            month_news_array = get_monthly_news_array(category, newspaper, year, month)
            if len(month_news_array) > 0:
                index = randint(0, len(month_news_array) - 1) # Picks one random news from the month
                create_news_file(month_news_array, index)


# MAIN
print_presentation()

process_el_observador()
process_la_diaria()
process_busqueda()

print_finish()
