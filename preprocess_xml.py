# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import errno

def split_xml_add_doc_structure (filepath_xml):
	tree = ET.parse(filepath_xml)
	root = tree.getroot()
	data = {}
	for doc in root:
		for field in doc:
			#HALP! try on datetime converter
			if (field.get('name') == 'fecha') and (field.text != '2000-00-00T00:00:00Z'):
				news_date = datetime.strptime(field.text, '%Y-%m-%dT%H:%M:%SZ')
				year = news_date.year
				month = news_date.month
				if (data.get(year) == None):
					data[year] = {}
				if (data[year].get(month) == None):
					data[year][month] = list()
				
				data[year][month].append(doc)
	return data

def dump_to_file(data):
	for year in data:
		for month in data[year]:
			root = ET.Element("add")
			for idx, doc in enumerate(data[year][month]):
				root.insert(idx, doc)
			tree = ET.ElementTree(root)
			file_path = os.path.join("./news", "processed", str(year), str(month), "la_republica.xml")
			
			#create folder if doesnt exist
			if not os.path.exists(os.path.dirname(file_path)):
				try:
					os.makedirs(os.path.dirname(file_path))
				except OSError as exc: # Guard against race condition
					if exc.errno != errno.EEXIST:
						raise
						
			tree.write(open(file_path, 'wb'), encoding="utf-8")
			# for field in doc:
			#   if field.get('name') == 'fecha':
			#     print(field.text)


#  MAIN
print( "Just a sec...")
# hacer para cada diario, por ahora solo la republica
data_la_republica = split_xml_add_doc_structure("./news/la_republica/2011_2014_la_republica.xml")

dump_to_file(data_la_republica)
