# -*- coding: utf-8 -*-
import csv
import json
import re
import sys
import xml.etree.ElementTree as ET

import settings
from helper_methods import month_year_iter

def generate_array_with_news():
    
    documents = []   
    documents_date = [] 
    for paper  in settings.NEWSPAPERS:            
        # No se va a usar porque se tienen pocos años
        date_from = settings.NEWSPAPERS[paper]['datefrom']
        date_to = settings.NEWSPAPERS[paper]['dateto']
        date_iter = month_year_iter(date_from, date_to)
        
        for date in date_iter:            
            year, month_not_general = date[0], date[1]
            month = month_not_general
            if paper == "el_observador":                
                if (month_not_general < 10):
                    month = "0" + str(month_not_general)
                else:
                    month = str(month_not_general)
            elif paper == "busqueda":
                month = month_not_general - 1
            path = settings.NEWS_JSON_FILEPATH.format(paper, str(year), str(month))
            with open(path, 'r+', encoding='utf-8') as data_file:
                tree = json.load(data_file)
            json_root = tree['add']                        
            for doc in json_root:
                if doc is not None and doc['doc'] is not None and doc['doc']['articulo'] != "":
                    article = doc['doc']['articulo'].lower()
                    if check_if_news_is_eu(article):
                        documents.append(format_news_content(article))                        
                        documents_date.append(str(month) + "/" + str(year))
    return documents, documents_date

def check_if_news_is_eu(article):    
    is_eu = False    

    if ((any(find_whole_word(word)(article) for word in settings.TERMS_BAG[0]["values"]))        
        and (any(find_whole_word(word)(article) for word in settings.TERMS_BAG[1]["values"]))):
            is_eu = True
    
    return is_eu

def find_whole_word(word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search

def format_news_content(original_content):
    original_content = cleanhtml(original_content)
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

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext