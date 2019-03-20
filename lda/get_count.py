import csv
import settings
settings.init()

def get_count_terms_csv ():
    terms = {}
    with open(settings.TERMS_FILEPATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        for row in csv_reader:
            for term in row:
                if term in terms:
                    terms[term] = terms[term] + 1
                else:
                    terms[term]= 1

    with open(settings.TERMS_COUNT_FILEPATH, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for term in terms:
            csv_writer.writerow([term, terms[term]])
            
get_count_terms_csv()