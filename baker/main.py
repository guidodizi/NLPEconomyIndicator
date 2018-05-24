# -*- coding: utf-8 -*-
import news_processor
import results_processor

# AUXILIAR METHODS
def print_presentation():
    print (u"\n---------------------------------------------------------------")
    print (u"---------------------------------------------------------------")
    print (u"Bienvenido al Indicador de Incertidumbre Económica para Uruguay")

def newspaper_input_options():
    print (u"\nIndique la opción del diario que desea procesar.")
    print (u"  1 - El Observador")
    print (u"  2 - El País")
    print (u"  3 - La Diaria")
    print (u"  4 - La República")
    print (u"  S - Salir\n")
    return input("Opción: ")

def print_processing_message(newspaper):
    print(u"\nSe está obteniendo el Indicador de Incertidumbre Económica para:")
    if (newspaper == "el_observador"):
        print(u"  - Diario: El Observador")
    elif (newspaper == "el_pais"):
        print(u"  - Diario: El País")
    elif (newspaper == "la_diaria"):
        print(u"  - Diario: La Diaria")
    elif (newspaper == "la_republica"):
        print(u"  - Diario: La República")
    print(u"\nAguarde unos instantes...")

def print_finish():
    print (u"\n¡Procesamiento finalizado!")
    print (u"Puede ver los resultados en la carpeta \"/baker/results\" \n")

def is_integer(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def newspaper_input_section():
    input_ok = False
    newspaper = ""
    input_newspaper = newspaper_input_options()
    while not input_ok:
        if input_newspaper == "S" or input_newspaper == "s":
            exit()
        elif input_newspaper == "1":
            newspaper = "el_observador"
            input_ok = True
        elif input_newspaper == "2":
            newspaper = "el_pais"
            input_ok = True
        elif input_newspaper == "3":
            newspaper = "la_diaria"
            input_ok = True
        elif input_newspaper == "4":
            newspaper = "la_republica"
            input_ok = True
        else:
            print ("\nOpción inválida.\n")
            input_newspaper = newspaper_input_options()
    return newspaper

def process_news(newspaper):
    if (newspaper == "el_pais"):
        news_processor.process_el_pais()
    elif (newspaper == "el_observador"):
        news_processor.process_el_observador()
    elif (newspaper == "la_diaria"):
        news_processor.process_la_diaria()     
    elif (newspaper == "la_republica"):
        news_processor.process_la_republica()

def scale_results_to_relative_month_count(newspaper):
    print(u"\nProcesamiento de noticias finalizado.")
    print(u"\nAguarde mientras se normalizan los resultados ...")
    results_processor.scale_to_relative_count(newspaper)

def scale_results_to_unit_standard_deviation(newspaper):
    results_processor.scale_to_unit_standard_deviation(newspaper)


# MAIN
print_presentation()

# Input sections
newspaper = newspaper_input_section()

print_processing_message(newspaper)

# Execute news processing (generate raw results)
process_news(newspaper)

# Scale results by month articles count
scale_results_to_relative_month_count(newspaper)

# Standardize results to unit standard deviation
scale_results_to_unit_standard_deviation(newspaper)

print_finish()
