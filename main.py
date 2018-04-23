# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import json
from pprint import pprint
import indicador_incertidumbre

with open('bagOfWords.json') as data_file:
    bagOfWords = json.load(data_file)

print bagOfWords['concepts'][0]["values"]
tree = ET.parse('news/larepublica20141107112348Noticias.xml')
add = tree.getroot()

artQty = 0 
artWithEpuQty = 0 
for doc in add:
    for field in doc:   
        #if field.get('name') == 'title':
        #            title = field.text.lower().encode('utf-8')
        if field.get('name') == 'articulo':
            article = field.text.lower().encode('utf-8')
            if ( any(word.encode('utf-8') in article for word in bagOfWords['concepts'][0]["values"]) and 
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][1]["values"]) ) and ( 
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][2]["values"]) or 
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][3]["values"]) or
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][4]["values"]) or
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][5]["values"]) or
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][6]["values"]) or
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][7]["values"]) or
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][8]["values"]) or
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][9]["values"]) or
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][10]["values"]) or
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][11]["values"]) or
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][12]["values"]) or
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][13]["values"]) or
                any(word.encode('utf-8') in article for word in bagOfWords['concepts'][14]["values"])):
                artWithEpuQty += 1                    
        artQty += 1

print ("La cantidad de articulos total es: " + str(artQty))
print ("La cantidad de articulos con EPU es: " + str(artWithEpuQty))    

